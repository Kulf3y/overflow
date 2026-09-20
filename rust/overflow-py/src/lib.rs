use pyo3::prelude::*;
use regex::Regex;

#[pyfunction]
fn redact_emails(input: &str) -> (String, usize) {
    let re = Regex::new(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}").unwrap();
    let mut count = 0usize;
    let output = re
        .replace_all(input, |_caps: &regex::Captures| {
            count += 1;
            "[EMAIL_REDACTED]"
        })
        .to_string();
    (output, count)
}

#[pymodule]
fn overflow_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(redact_emails, m)?)?;
    Ok(())
}
