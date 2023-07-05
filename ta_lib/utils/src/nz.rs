pub fn nz(source: &[Option<f64>], replacement: Option<f64>) -> Vec<f64> {
    let replacement = replacement.unwrap_or(0.0);
    source.iter().map(|&x| x.unwrap_or(replacement)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nz_with_replacement() {
        let source = vec![Some(1.0), None, Some(2.0), None];
        let replacement = Some(3.0);
        let expected = vec![1.0, 3.0, 2.0, 3.0];

        let result = nz(&source, replacement);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_nz_with_default_replacement() {
        let source = vec![Some(1.0), None, Some(2.0), None];
        let expected = vec![1.0, 0.0, 2.0, 0.0];

        let result = nz(&source, None);

        assert_eq!(result, expected);
    }
}
