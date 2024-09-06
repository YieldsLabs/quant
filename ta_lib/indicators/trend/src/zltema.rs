use core::prelude::*;

pub fn zltema(source: &Price, period: Period) -> Price {
    source
        .smooth(Smooth::TEMA, period)
        .smooth(Smooth::TEMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_zltema() {
        let source = Series::from([18.898, 18.838, 18.881, 18.925, 18.846]);
        let period = 3;
        let expected = vec![18.898, 18.852058, 18.865294, 18.910984, 18.869732];

        let result: Vec<Scalar> = zltema(&source, period).into();

        assert_eq!(result, expected);
    }
}
