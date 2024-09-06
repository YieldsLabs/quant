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

#[macro_export]
macro_rules! w {
    ($osc:expr, $lower_const:expr, $upper_const:expr) => {{
        let prev_osc = $osc.shift(1);
        let osc_2_back = $osc.shift(2);
        let osc_3_back = $osc.shift(3);
        let osc_4_back = $osc.shift(4);
        let osc_5_back = $osc.shift(5);

        (
            $osc.sgt(&$lower_const)
                & prev_osc.slt(&$lower_const)
                & prev_osc.slt(&osc_2_back)
                & osc_2_back.slt(&$lower_cons)
                & osc_2_back.sgt(&osc_3_back)
                & osc_3_back.slt(&$lower_cons)
                & osc_3_back.slt(&osc_4_back)
                & osc_4_back.slt(&$lower_cons)
                & osc_5_back.sgt(&$lower_cons),
            $osc.slt(&$upper_const)
                & prev_osc.sgt(&$upper_const)
                & prev_osc.sgt(&osc_2_back)
                & osc_2_back.sgt(&$upper_const)
                & osc_2_back.slt(&osc_3_back)
                & osc_3_back.sgt(&$upper_const)
                & osc_3_back.sgt(&osc_4_back)
                & osc_4_back.sgt(&$upper_const)
                & osc_5_back.slt(&$upper_const),
        )
    }};
}
