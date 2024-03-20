use core::prelude::*;

pub fn zltema(source: &Series<f32>, period: usize) -> Series<f32> {
    let ema1 = source.smooth(Smooth::EMA, period);
    let ema2 = ema1.smooth(Smooth::EMA, period);
    let ema3 = ema2.smooth(Smooth::EMA, period);

    let tema = 3. * (ema1 - ema2) + ema3;

    let tema1 = tema.smooth(Smooth::EMA, period);
    let tema2 = tema1.smooth(Smooth::EMA, period);
    let tema3 = tema2.smooth(Smooth::EMA, period);

    3. * (tema1 - tema2) + tema3
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zltema() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let expected = vec![18.898, 18.852058, 18.865294, 18.910984, 18.869732];

        let result: Vec<f32> = zltema(&source, period).into();

        assert_eq!(result, expected);
    }
}
