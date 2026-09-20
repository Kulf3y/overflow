pub mod redaction;

pub const NAME: &str = "overflow-core";

pub fn sanitize_text(input: &str) -> redaction::RedactionReport {
    redaction::redact_emails(input)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sanitize_text_redacts_email() {
        let report = sanitize_text("user@example.com");
        assert_eq!(report.emails_found, 1);
        assert!(report.output.contains("[EMAIL_REDACTED]"));
    }

    #[test]
    fn sanitize_text_leaves_normal_text() {
        let report = sanitize_text("hello world");
        assert_eq!(report.emails_found, 0);
        assert_eq!(report.output, "hello world");
    }
}
