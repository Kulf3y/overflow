use regex::Regex;

pub struct RedactionReport {
    pub output: String,
    pub emails_found: usize,
}

pub fn redact_emails(input: &str) -> RedactionReport {
    let pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}";
    let re = Regex::new(pattern).expect("email regex should compile");
    let mut count = 0usize;

    let output = re
        .replace_all(input, |_caps: &regex::Captures| {
            count += 1;
            "[EMAIL_REDACTED]"
        })
        .to_string();

    RedactionReport {
        output,
        emails_found: count,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn redacts_simple_email() {
        let report = redact_emails("Contact me at jane.doe@example.com");
        assert_eq!(report.emails_found, 1);
        assert!(report.output.contains("[EMAIL_REDACTED]"));
        assert!(!report.output.contains("jane.doe@example.com"));
    }

    #[test]
    fn redacts_multiple_emails() {
        let report = redact_emails("a@example.com and b@example.org");
        assert_eq!(report.emails_found, 2);
    }

    #[test]
    fn leaves_text_without_email() {
        let report = redact_emails("No contact here");
        assert_eq!(report.emails_found, 0);
        assert_eq!(report.output, "No contact here");
    }
}
