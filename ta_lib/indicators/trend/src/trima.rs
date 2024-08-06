use core::prelude::*;

pub fn trima(source: &Series<f32>, period: usize) -> Series<f32> {
    let half_period = 0.5 * period as f32;

    let n = half_period.ceil() as usize;
    let m = (half_period.floor() + 1.) as usize;

    source.smooth(Smooth::SMA, n).smooth(Smooth::SMA, m)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trima() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.25, 2.0, 3.0, 4.0];

        let result: Vec<f32> = trima(&source, 3).into();

        assert_eq!(result, expected);
    }
}
