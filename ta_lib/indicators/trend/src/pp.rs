use core::prelude::*;

pub fn pp(high: &Price, low: &Price, close: &Price) -> (Price, Price) {
    let pp = (high + low + close) / 3.;

    let support = 2. * &pp - high;
    let resistance = 2. * &pp - low;

    (support, resistance)
}

pub fn fpp(high: &Price, low: &Price, close: &Price) -> (Price, Price) {
    let pp = (high + low + close) / 3.;

    let hl = 0.382 * (high - low);

    let support = &pp - &hl;
    let resistance = &pp + &hl;

    (support, resistance)
}

pub fn wpp(open: &Price, high: &Price, low: &Price) -> (Price, Price) {
    let pp = (high + low + 2. * open) / 4.;

    let support = 2. * &pp - high;
    let resistance = 2. * &pp - low;

    (support, resistance)
}

pub fn cpp(high: &Price, low: &Price, close: &Price) -> (Price, Price) {
    let hl = 1.1 * (high - low) / 12.;

    let support = close - &hl;
    let resistance = close + &hl;

    (support, resistance)
}

pub fn dpp(open: &Price, high: &Price, low: &Price, close: &Price) -> (Price, Price) {
    let mut pp = iff!(
        close.sgt(open),
        2. * high + low + close,
        high + low + 2. * close
    );
    pp = iff!(close.slt(open), high + 2. * low + close, pp);

    let support = 0.5 * &pp - high;
    let resistance = 0.5 * &pp - low;

    (support, resistance)
}

pub fn spp(
    high: &Price,
    low: &Price,
    close: &Price,
    smooth: Smooth,
    period: Period,
) -> (Price, Price) {
    let hh = high.highest(period);
    let ll = low.lowest(period);
    let close = close.smooth(smooth, period);

    let pp = (&hh + &ll + close) / 3.;

    let support = 2. * pp.lowest(period) - hh;
    let resistance = 2. * pp.highest(period) - ll;

    (support, resistance)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pivot_points() {
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);
        let expected_support = vec![
            6.5439324, 6.5541005, 6.5118666, 6.4641, 6.5020003, 6.526467, 6.5022664, 6.5202003,
            6.5273, 6.5162005, 6.4905, 6.4427676, 6.469, 6.4663997, 6.4966, 6.5126,
        ];
        let expected_resistance = vec![
            6.5621324, 6.6196003, 6.575967, 6.54, 6.5438004, 6.583367, 6.5526667, 6.538, 6.5564,
            6.5413003, 6.5248, 6.4932675, 6.4941998, 6.5401993, 6.5205, 6.5354,
        ];

        let (support, resistance) = pp(&high, &low, &close);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_fibonacci_pivot_points() {
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);
        let expected_support = vec![
            6.545014, 6.554479, 6.5285473, 6.4801064, 6.5000324, 6.526498, 6.5133805, 6.5214005,
            6.527384, 6.522512, 6.4983974, 6.455343, 6.4681735, 6.481808, 6.49627, 6.5122905,
        ];
        let expected_resistance = vec![
            6.5589185, 6.6045213, 6.5775194, 6.5380936, 6.531968, 6.569969, 6.551886, 6.535,
            6.549616, 6.5416884, 6.5246024, 6.4939246, 6.4874263, 6.5381913, 6.51453, 6.5297093,
        ];

        let (support, resistance) = fpp(&high, &low, &close);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_woodie_pivot_points() {
        let open = Series::from([
            6.5541, 6.5942, 6.5345, 6.4950, 6.5298, 6.5619, 6.5223, 6.5300, 6.5451, 6.5254, 6.5038,
            6.4614, 6.4853, 6.4966, 6.5117, 6.5272,
        ]);
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let expected_support = vec![
            6.5449996, 6.5614505, 6.50245, 6.4570503, 6.5089, 6.5334506, 6.4970994, 6.5211005,
            6.53055, 6.5128503, 6.48665, 6.43615, 6.4727, 6.4597, 6.49975, 6.5158005,
        ];
        let expected_resistance = vec![
            6.5631995, 6.6269503, 6.5665503, 6.5329504, 6.5507, 6.5903506, 6.5474997, 6.5389004,
            6.55965, 6.53795, 6.52095, 6.48665, 6.4979, 6.5334997, 6.52365, 6.5386004,
        ];

        let (support, resistance) = wpp(&open, &high, &low);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_camarilla_pivot_points() {
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);
        let expected_support = vec![
            6.5524316, 6.588196, 6.528924, 6.4880424, 6.525968, 6.5563846, 6.5176797, 6.5283685,
            6.5425324, 6.5230994, 6.5006557, 6.456771, 6.4830904, 6.4898353, 6.509509, 6.52491,
        ];
        let expected_resistance = vec![
            6.5557685, 6.6002045, 6.540676, 6.5019574, 6.533632, 6.566816, 6.52692, 6.531632,
            6.5478673, 6.527701, 6.506944, 6.466029, 6.48771, 6.503365, 6.513891, 6.52909,
        ];

        let (support, resistance) = cpp(&high, &low, &close);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_demark_pivot_points() {
        let open = Series::from([
            6.5541, 6.5942, 6.5345, 6.4950, 6.5298, 6.5619, 6.5223, 6.5300, 6.5451, 6.5254, 6.5038,
            6.4614, 6.4853, 6.4866, 6.5117, 6.5272,
        ]);
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);
        let expected_support = vec![
            6.5449996, 6.5614505, 6.5324497, 6.4570503, 6.5089, 6.5089, 6.4970994, 6.5211005,
            6.5329, 6.5128503, 6.48665, 6.43615, 6.473401, 6.4881997, 6.49975, 6.5053997,
        ];
        let expected_resistance = vec![
            6.5631995, 6.6269503, 6.59655, 6.5329504, 6.5507, 6.5658, 6.5474997, 6.5389004, 6.562,
            6.53795, 6.52095, 6.48665, 6.498601, 6.5619993, 6.52365, 6.5281997,
        ];

        let (support, resistance) = dpp(&open, &high, &low, &close);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }

    #[test]
    fn test_smooth_pivot_points() {
        let high = Series::from([
            6.5600, 6.6049, 6.5942, 6.5541, 6.5300, 6.5700, 6.5630, 6.5362, 6.5497, 6.5480, 6.5325,
            6.5065, 6.4866, 6.5536, 6.5142, 6.5294,
        ]);
        let low = Series::from([
            6.5418, 6.5394, 6.5301, 6.4782, 6.4882, 6.5131, 6.5126, 6.5184, 6.5206, 6.5229, 6.4982,
            6.4560, 6.4614, 6.4798, 6.4903, 6.5066,
        ]);
        let close = Series::from([
            6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452, 6.5254, 6.5038,
            6.4614, 6.4854, 6.4966, 6.5117, 6.5270,
        ]);

        let period = 3;

        let expected_support = vec![
            6.5439324, 6.4990325, 6.4990325, 6.4780555, 6.467311, 6.4813333, 6.4813333, 6.4813333,
            6.5010676, 6.518056, 6.498766, 6.452577, 6.448855, 6.427755, 6.427755, 6.440223,
        ];
        let expected_resistance = vec![
            6.5621324, 6.6062336, 6.615534, 6.6674337, 6.6524887, 6.6047554, 6.5758677, 6.5677786,
            6.5677786, 6.5619783, 6.5738664, 6.611756, 6.592466, 6.544577, 6.5471992, 6.55031,
        ];

        let (support, resistance) = spp(&high, &low, &close, Smooth::SMA, period);
        let result_support: Vec<Scalar> = support.into();
        let result_resistance: Vec<Scalar> = resistance.into();

        assert_eq!(result_support, expected_support);
        assert_eq!(result_resistance, expected_resistance);
    }
}
