use core::iff;
use core::Series;

pub fn kama(source: &Series<f32>, period: usize) -> Series<f32> {
    let len = source.len();
    let change = source.change(period).abs();
    let volatility = source.change(1).abs().sum(period);

    let er = change / volatility;

    let alpha = iff!(
        er.na(),
        Series::fill(len, 2.0 / (period as f32 + 1.0)),
        (er * 0.666_666_7).sqrt()
    );

    let mut kama = Series::zero(len);

    for _ in 0..len {
        let prev_kama = kama.shift(1);

        kama = iff!(
            prev_kama.na(),
            source,
            &prev_kama + &alpha * (source - &prev_kama)
        )
    }

    kama
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kama() {
        let source = Series::from([19.099, 19.079, 19.074, 19.139, 19.191]);
        let expected = vec![19.099, 19.089, 19.081501, 19.112799, 19.173977];

        let result: Vec<f32> = kama(&source, 3).into();

        assert_eq!(result, expected);
    }
}
