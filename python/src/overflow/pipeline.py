from dataclasses import dataclass, field

from overflow.optimizer import optimize_text
from overflow.policy import validate_policy
from overflow.privacy import redact_text
from overflow.providers import MockProvider
from overflow.security import scan_text


@dataclass
class PipelineResult:
    allowed: bool
    output_text: str
    response_text: str
    reasons: list[str] = field(default_factory=list)
    privacy_counts: dict[str, int] = field(default_factory=dict)
    security_counts: dict[str, int] = field(default_factory=dict)
    optimization: dict = field(default_factory=dict)
    provider: str = "none"


def process_text(
    text,
    policy=None,
    custom_patterns=None,
    optimize=True,
    audit_enabled=False,
    audit_path=None,
    provider=None
):
    reasons = []

    privacy_report = redact_text(text, custom_patterns=custom_patterns)
    security_report = scan_text(privacy_report.output)

    if not security_report.allowed:
        reasons.extend(security_report.reasons)

    if policy is not None:
        policy_errors = validate_policy(policy)

        if policy_errors:
            reasons.append("Policy validation failed.")

    if reasons:
        return PipelineResult(
            allowed=False,
            output_text=privacy_report.output,
            response_text="",
            reasons=reasons,
            privacy_counts=privacy_report.counts,
            security_counts=security_report.counts,
            optimization={},
            provider="none"
        )

    safe_text = privacy_report.output
    optimization_report = None

    if optimize:
        optimization_report = optimize_text(safe_text)
        safe_text = optimization_report.output

    if provider is None:
        provider = MockProvider()

    provider_result = provider.complete(safe_text)

    optimization_data = {}

    if optimization_report is not None:
        optimization_data = {
            "original_tokens": optimization_report.original_tokens,
            "optimized_tokens": optimization_report.optimized_tokens,
            "reduction_percent": optimization_report.reduction_percent
        }

    if audit_enabled:
        from overflow.audit import AuditChain

        chain = AuditChain(audit_path)

        chain.log_event(
            "pipeline.request",
            metadata={
                "allowed": True,
                "provider": provider_result.provider,
                "privacy_counts": privacy_report.counts,
                "security_counts": security_report.counts,
                "optimized": optimize
            }
        )

    return PipelineResult(
        allowed=True,
        output_text=safe_text,
        response_text=provider_result.text,
        reasons=[],
        privacy_counts=privacy_report.counts,
        security_counts=security_report.counts,
        optimization=optimization_data,
        provider=provider_result.provider
    )
