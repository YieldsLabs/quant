use core::series::Series;

pub fn gma(source: &[f32], period: usize) -> Series<f32> {
    let source = Series::from(source);

    

    source.log().ma(period).exp()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let expected = vec![1.0, std::f32::consts::SQRT_2, 1.8171206, 2.8844993, 3.9148676];

        let result: Vec<f32> = gma(&source, 3).into();

        assert_eq!(result, expected);
    }
}
