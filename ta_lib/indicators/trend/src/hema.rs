use core::prelude::*;

pub fn hema(source: &Series<f32>, period: usize) -> Series<f32> {
    let period = (period as f32 / 2.) as usize;

    3. * source.smooth(Smooth::WMA, period) - 2. * source.smooth(Smooth::EMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hema() {
        let source = Series::from([19.099, 19.079, 19.074, 19.139, 19.191]);
        let expected = vec![19.099003, 19.08567, 19.07122, 19.114738, 19.18724];
        let period = 4;

        let result: Vec<f32> = hema(&source, period).into();

        assert_eq!(result, expected);
    }
}
