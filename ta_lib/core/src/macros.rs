#[macro_export]
macro_rules! iff {
    ($cond:expr, $if_true:expr, $if_false:expr) => {{
        $cond
            .iter()
            .zip($if_true.iter())
            .zip($if_false.iter())
            .map(|((cond_val, true_val), false_val)| match cond_val {
                Some(true_condition) if *true_condition => *true_val,
                _ => *false_val,
            })
            .collect::<Series<_>>()
    }};
}

#[macro_export]
macro_rules! nz {
    ($source:expr, $fill:expr) => {{
        $source
            .iter()
            .zip($fill.iter())
            .map(|(source, fill)| match source {
                Some(val) => Some(*val),
                _ => *fill,
            })
            .collect::<Series<_>>()
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

    #[test]
    fn test_nz() {
        let source = Series::from([f32::NAN, 5.0, 4.0, 3.0, 5.0]);
        let fill = Series::from([1.0, 0.5, 5.0, 2.0, 8.0]);

        let expected = Series::from([1.0, 5.0, 4.0, 3.0, 5.0]);

        let result = nz!(source, fill);

        assert_eq!(result, expected);
    }
}
