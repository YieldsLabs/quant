use core::prelude::*;

pub fn tma(source: &Series<f32>, period: usize) -> Series<f32> {
    let n = (period as f32 / 2.).signum() as usize;
    let m = (period as f32 / 2. + 1.) as usize;

    source.smooth(Smooth::SMA, n).smooth(Smooth::SMA, m)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tma() {
        let source = Series::from([1.0, 2.0, 3.0, 4.0, 5.0]);
        let expected = vec![1.0, 1.5, 2.5, 3.5, 4.5];

        let result: Vec<f32> = tma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
