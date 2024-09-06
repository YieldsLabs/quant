use core::prelude::*;

pub fn dema(source: &Price, period: Period) -> Price {
    source.smooth(Smooth::DEMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dema() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.75, 2.75, 3.8125, 4.875];

        let result: Vec<f32> = dema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
