use core::Series;

pub fn ppb(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
    factor: f32,
) -> (Series<f32>, Series<f32>, Series<f32>) {
    let hstd = high.std(period);
    let lstd = low.std(period);

    let ppvih = hstd.highest(period) * factor;
    let ppvil = lstd.lowest(period) * factor;

    let middle_band = close.ma(period);

    let upper_band = &middle_band + ppvih;
    let lower_band = &middle_band - ppvil;

    (upper_band, middle_band, lower_band)
}

#[test]
fn test_ppb() {
    let high = Series::from([
        19.129, 19.116, 19.154, 19.195, 19.217, 19.285, 19.341, 19.394, 19.450,
    ]);
    let low = Series::from([
        19.090, 19.086, 19.074, 19.145, 19.141, 19.155, 19.219, 19.306, 19.355,
    ]);
    let close = Series::from([
        19.102, 19.100, 19.146, 19.181, 19.155, 19.248, 19.309, 19.355, 19.439,
    ]);
    let factor = 2.0;
    let period = 3;
    let epsilon = 0.0001;
    let expected_upper_band = [
        19.102, 19.114, 19.147537, 19.206852, 19.225185, 19.271284, 19.338737, 19.405405, 19.46907,
    ];
    let expected_middle_band = [
        19.102, 19.101, 19.116, 19.142332, 19.160666, 19.194666, 19.237333, 19.304, 19.367666,
    ];
    let expected_lower_band = [
        19.102, 19.101, 19.116, 19.138332, 19.147068, 19.18289, 19.225557, 19.292225, 19.299759,
    ];

    let (upper_band, middle_band, lower_band) = ppb(&high, &low, &close, period, factor);

    let result_upper_band: Vec<f32> = upper_band.into();
    let result_middle_band: Vec<f32> = middle_band.into();
    let result_lower_band: Vec<f32> = lower_band.into();

    for i in 0..high.len() {
        let a = result_upper_band[i];
        let b = expected_upper_band[i];
        assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

        let a = result_middle_band[i];
        let b = expected_middle_band[i];
        assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);

        let a = result_lower_band[i];
        let b = expected_lower_band[i];
        assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b);
    }
}
