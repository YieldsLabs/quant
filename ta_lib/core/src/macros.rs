#[macro_export]
macro_rules! iff {
    ($cond:expr, $if_true:expr, $if_false:expr) => {{
        let data = $cond
            .into_iter()
            .zip($if_true.clone().into_iter())
            .zip($if_false.clone().into_iter())
            .map(|((cond_val, true_val), false_val)| match cond_val {
                Some(true_condition) if true_condition => true_val.unwrap_or(f32::NAN),
                _ => false_val.unwrap_or(f32::NAN),
            })
            .collect::<Vec<_>>();

        Series::from(data)
    }};
}

#[cfg(test)]
mod tests {
    use crate::{Comparator, Series};

    #[test]
    fn test_iff() {
        let a = Series::from([2.0, 5.0, 4.0, 3.0, 5.0]);
        let b = Series::from([1.0, 0.5, 5.0, 2.0, 8.0]);
        let one = Series::fill(1.0, a.len());
        let minus_one = Series::fill(-1.0, a.len());
        let cond = a.sgt(&b);

        let expected = Series::from([1.0, 1.0, -1.0, 1.0, -1.0]);

        let result = iff!(cond, one, minus_one);

        assert_eq!(result, expected);
    }
}
