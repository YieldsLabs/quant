use core::prelude::*;

pub fn ema(source: &Price, period: Period) -> Price {
    source.smooth(Smooth::EMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ema() {
        let source = Series::from([
            6.5232, 6.5474, 6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452,
            6.5254, 6.5038, 6.4614, 6.4854, 6.4966,
        ]);
        let expected = vec![
            6.5232, 6.5353003, 6.5447, 6.5694504, 6.552125, 6.5235624, 6.526681, 6.544141,
            6.5332203, 6.5316105, 6.5384054, 6.531903, 6.5178514, 6.489626, 6.487513, 6.492057,
        ];

        let result: Vec<Scalar> = ema(&source, 3).into();

        assert_eq!(result, expected);
    }
}
