#[macro_export]
macro_rules! a {
    ($upper_band:expr, $lower_band:expr, $source:expr) => {{
        let prev_source = $source.shift(1);

        (
            $source.slt(&$lower_band) & prev_source.sgt(&$lower_band.shift(1)),
            $source.sgt(&$upper_band) & prev_source.slt(&$upper_band.shift(1)),
        )
    }};
}

#[macro_export]
macro_rules! c {
    ($upper_band:expr, $middle_band:expr, $lower_band:expr, $source:expr) => {{
        let prev_source = $source.shift(1);

        (
            $source.sgt(&$lower_band)
                & prev_source.slt(&$lower_band.shift(1))
                & $source.slt(&$middle_band),
            $source.slt(&$upper_band)
                & prev_source.sgt(&$upper_band.shift(1))
                & $source.sgt(&$middle_band),
        )
    }};
}

#[macro_export]
macro_rules! r {
    ($upper_band:expr, $lower_band:expr, $source:expr) => {{
        let prev_source = $source.shift(1);
        let back_2_source = $source.shift(2);
        let back_3_source = $source.shift(3);
        let back_4_source = $source.shift(4);
        let back_5_source = $source.shift(5);

        (
            $source.sgt(&$lower_band)
                & prev_source.slt(&$lower_band.shift(1))
                & back_2_source.slt(&$lower_band.shift(2))
                & back_3_source.slt(&$lower_band.shift(3))
                & back_4_source.slt(&$lower_band.shift(4))
                & back_5_source.slt(&$lower_band.shift(5)),
            $source.slt(&$upper_band)
                & prev_source.sgt(&$upper_band.shift(1))
                & back_2_source.sgt(&$upper_band.shift(2))
                & back_3_source.sgt(&$upper_band.shift(3))
                & back_4_source.sgt(&$upper_band.shift(4))
                & back_5_source.sgt(&$upper_band.shift(5)),
        )
    }};
}
