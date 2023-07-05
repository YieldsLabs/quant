pub fn change(source: &[f64], length: usize) -> Vec<f64> {
    let len = source.len();
    let mut change = vec![0.0; len];

    if length > len {
        return change;
    }

    for i in length..len {
        change[i] = source[i] - source[i - length];
    }

    change
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_change() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let length = 2;
        let expected = vec![0.0, 0.0, 2.0, 2.0, 2.0];

        let result = change(&source, length);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_change_zero_length() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let length = 0;
        let expected = vec![0.0, 0.0, 0.0, 0.0, 0.0];

        let result = change(&source, length);

        assert_eq!(result, expected);
    }
}
