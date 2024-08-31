use core::prelude::*;

pub fn trima(source: &Price, period: Period) -> Price {
    let period_half = HALF * period as Scalar;

    let n = period_half.ceil() as Period;
    let m = (period_half.floor() + 1.) as Period;

    source.smooth(Smooth::SMA, n).smooth(Smooth::SMA, m)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trima() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.25, 2.0, 3.0, 4.0];

        let result: Vec<Scalar> = trima(&source, 3).into();

        assert_eq!(result, expected);
    }
}
