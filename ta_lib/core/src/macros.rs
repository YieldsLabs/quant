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
