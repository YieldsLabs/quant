pub fn highest(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();
    let mut highest_values = vec![None; len];

    if len < period {
        return highest_values;
    }

    for i in (period - 1)..len {
        let highest = *source[i + 1 - period..=i]
            .iter()
            .max_by(|x, y| x.partial_cmp(y).unwrap())
            .unwrap();
        highest_values[i] = Some(highest);
    }

    highest_values
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_highest() {
        let source = vec![1.0, 2.0, 3.0, 2.0, 1.0];
        let expected = vec![None, None, Some(3.0), Some(3.0), Some(3.0)];

        let result = highest(&source, 3);

        assert_eq!(result, expected);
    }
}
