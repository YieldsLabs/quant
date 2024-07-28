#[macro_export]
macro_rules! a {
    ($osc:expr, $lower_const:expr, $upper_const:expr) => {{
        let prev_osc = $osc.shift(1);

        (
            $osc.slt(&$lower_const) & prev_osc.sgt(&$lower_const),
            $osc.sgt(&$upper_const) & prev_osc.slt(&$upper_const),
        )
    }};
}

#[macro_export]
macro_rules! c {
    ($osc:expr, $lower_const:expr, $upper_const:expr) => {{
        let prev_osc = $osc.shift(1);

        (
            $osc.sgt(&$lower_const) & prev_osc.slt(&$lower_const),
            $osc.slt(&$upper_const) & prev_osc.sgt(&$upper_const),
        )
    }};
}

#[macro_export]
macro_rules! v {
    ($osc:expr, $lower_const:expr, $upper_const:expr) => {{
        let prev_osc = $osc.shift(1);
        let osc_2_back = $osc.shift(2);

        (
            $osc.sgt(&$lower_const) & prev_osc.slt(&$lower_const) & osc_2_back.sgt(&$lower_const),
            $osc.slt(&$upper_const) & prev_osc.sgt(&$upper_const) & osc_2_back.slt(&$upper_const),
        )
    }};
}
