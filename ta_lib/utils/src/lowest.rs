pub fn lowest(source: &[f64], period: usize) -> Vec<Option<f64>> {
    let len = source.len();
    let mut lowest_values = vec![None; len];

    if len < period {
        return lowest_values;
    }

    for i in (period - 1)..len {
        let lowest = *source[i + 1 - period..=i]
            .iter()
            .min_by(|x, y| x.partial_cmp(y).unwrap())
            .unwrap();
        lowest_values[i] = Some(lowest);
    }

    lowest_values
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lowest() {
        let source = vec![3.0, 2.0, 1.0, 2.0, 3.0];
        let expected = vec![None, None, Some(1.0), Some(1.0), Some(1.0)];

        let result = lowest(&source, 3);

        assert_eq!(result, expected);
    }
}
