use core::iff;
use core::Series;

pub fn kama(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);
    let change = source.change(period).abs();
    let volatility = source.change(1).abs().sum(period);

    let er = change / volatility;

    let alpha = iff!(
        er.na(),
        Series::empty(source.len()).nz(Some(2.0 / (period as f32 + 1.0))),
        (er * 0.666_666_7).sqrt()
    );

    let mut kama = Series::empty(source.len());

    for _ in 0..source.len() {
        let shifted = kama.shift(1);

        kama = iff!(
            shifted.na(),
            source,
            &shifted + &alpha * (&source - &shifted)
        )
    }

    kama
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kama() {
        let source = vec![19.099, 19.079, 19.074, 19.139, 19.191];
        let expected = vec![19.099, 19.089, 19.081501, 19.112799, 19.173977];

        let result: Vec<f32> = kama(&source, 3).into();

        assert_eq!(result, expected);
    }
}
