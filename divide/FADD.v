module FADD(
    // inputs
    input  [31:0] io_a, 
    input  [31:0] io_b, 
    input  [2:0] io_rm

    // outputs
    output [31:0] io_result, 
    output [4:0] io_fflags
);

    
    wire result_sign_nan[0: 0];
    wire result_exp_nan[7: 0];
    wire result_mant_nan[22: 0];
    wire result_exp_inf[7: 0];
    wire result_mant_inf[22: 0];
    wire result_exp_both_zero[7: 0];
    wire result_mant_both_zero[22: 0];
    wire result_exp_opposite[7: 0];
    wire result_mant_opposite[22: 0];
    wire sign_a[0: 0];
    wire exp_a[7: 0];
    wire mant_a[22: 0];
    wire sign_b[0: 0];
    wire exp_b[7: 0];
    wire mant_b[22: 0];
    wire result_sign_opposite[0: 0];
    wire result_sign_both_zero[0: 0];
    wire is_normal_a[0: 0];
    wire is_subnormal_a[0: 0];
    wire is_zero_a[0: 0];
    wire is_inf_a[0: 0];
    wire is_nan_a[0: 0];
    wire effective_subtraction[0: 0];
    wire small_add[0: 0];
    wire is_normal_b[0: 0];
    wire is_subnormal_b[0: 0];
    wire is_zero_b[0: 0];
    wire is_inf_b[0: 0];
    wire is_nan_b[0: 0];
    wire is_opposite[0: 0];
    wire mant_ext_a[23: 0];
    wire exp_ext_a[7: 0];
    wire result_sign_one_zero[0: 0];
    wire result_exp_one_zero[7: 0];
    wire result_mant_one_zero[22: 0];
    wire result_sign_inf[0: 0];
    wire is_Snan_a[0: 0];
    wire mant_ext_b[23: 0];
    wire exp_ext_b[7: 0];
    wire is_both_zero[0: 0];
    wire is_Snan_b[0: 0];
    wire is_nan[0: 0];
    wire exp_diff[7: 0];
    wire aligned_exp[7: 0];
    wire need_swap[0: 0];
    wire is_one_zero[0: 0];
    wire special_flag[0: 0];
    wire is_inf[0: 0];
    wire shift_too_large[0: 0];
    wire shift_smaller[25: 0];
    wire aligned_mant_larger[27: 0];
    wire resultant_sign[0: 0];
    wire special_result[31: 0];
    wire special_case_happen[0: 0];
    wire main[25: 0];
    wire smaller_sticky[0: 0];
    wire rmin[0: 0];
    wire aligned_mant_smaller[27: 0];
    wire overflow_result[31: 0];
    wire adder_result[27: 0];
    wire carry_out[0: 0];
    wire implied_bit[0: 0];
    wire computed_shift[4: 0];
    wire cancellation[0: 0];
    wire keep[0: 0];
    wire real_shift_norm[4: 0];
    wire adjusted_exp[7: 0];
    wire normalized_mantissa[26: 0];
    wire normalized_exp[7: 0];
    wire rounding_input[22: 0];
    wire f1[0: 0];
    wire f2[0: 0];
    wire f3[0: 0];
    wire inexact_flag[0: 0];
    wire round_up[0: 0];
    wire n_carry_out[0: 0];
    wire rounded_mantissa[22: 0];
    wire rounded_exp[7: 0];
    wire tiny[0: 0];
    wire overflow[0: 0];
    wire normal_result[31: 0];
    wire inexact[0: 0];
    wire underflow[0: 0];

    // assignments
    wire result_sign_nan_0 = 0b0;
    assign result_sign_nan = result_sign_nan_0;

    wire result_exp_nan_0 = 0xFF;
    assign result_exp_nan = result_exp_nan_0;

    wire result_mant_nan_0 = 0b10000000000000000000000;
    assign result_mant_nan = result_mant_nan_0;

    wire result_exp_inf_0 = 0xFF;
    assign result_exp_inf = result_exp_inf_0;

    wire result_mant_inf_0 = 0b0;
    assign result_mant_inf = result_mant_inf_0;

    wire result_exp_both_zero_0 = 0b0;
    assign result_exp_both_zero = result_exp_both_zero_0;

    wire result_mant_both_zero_0 = 0b0;
    assign result_mant_both_zero = result_mant_both_zero_0;

    wire result_exp_opposite_0 = 0b0;
    assign result_exp_opposite = result_exp_opposite_0;

    wire result_mant_opposite_0 = 0b0;
    assign result_mant_opposite = result_mant_opposite_0;

    wire sign_a_0 = io_a[31];
    assign sign_a = sign_a_0;

    wire exp_a_0 = io_a[30: 23];
    assign exp_a = exp_a_0;

    wire mant_a_0 = io_a[22: 0];
    assign mant_a = mant_a_0;

    wire sign_b_0 = io_b[31];
    assign sign_b = sign_b_0;

    wire exp_b_0 = io_b[30: 23];
    assign exp_b = exp_b_0;

    wire mant_b_0 = io_b[22: 0];
    assign mant_b = mant_b_0;

    wire result_sign_opposite_0 = 0b010;
    wire result_sign_opposite_1 = io_rm == result_sign_opposite_0;
    wire result_sign_opposite_2 = 0b1;
    wire result_sign_opposite_3 = 0b0;
    wire result_sign_opposite_4 = result_sign_opposite_1? result_sign_opposite_2 : result_sign_opposite_3;
    assign result_sign_opposite = result_sign_opposite_4;

    assign result_sign_both_zero = sign_a;

    wire is_normal_a_0 = 0b0;
    wire is_normal_a_1 = exp_a != is_normal_a_0;
    wire is_normal_a_2 = 0b0;
    wire is_normal_a_3 = mant_a != is_normal_a_2;
    wire is_normal_a_4 = is_normal_a_1 && is_normal_a_3;
    assign is_normal_a = is_normal_a_4;

    wire is_subnormal_a_0 = 0b0;
    wire is_subnormal_a_1 = exp_a == is_subnormal_a_0;
    wire is_subnormal_a_2 = 0b0;
    wire is_subnormal_a_3 = mant_a != is_subnormal_a_2;
    wire is_subnormal_a_4 = is_subnormal_a_1 && is_subnormal_a_3;
    assign is_subnormal_a = is_subnormal_a_4;

    wire is_zero_a_0 = 0b0;
    wire is_zero_a_1 = exp_a == is_zero_a_0;
    wire is_zero_a_2 = 0b0;
    wire is_zero_a_3 = mant_a == is_zero_a_2;
    wire is_zero_a_4 = is_zero_a_1 && is_zero_a_3;
    assign is_zero_a = is_zero_a_4;

    wire is_inf_a_0 = 0xFF;
    wire is_inf_a_1 = exp_a == is_inf_a_0;
    wire is_inf_a_2 = 0b0;
    wire is_inf_a_3 = mant_a == is_inf_a_2;
    wire is_inf_a_4 = is_inf_a_1 && is_inf_a_3;
    assign is_inf_a = is_inf_a_4;

    wire is_nan_a_0 = 0xFF;
    wire is_nan_a_1 = exp_a == is_nan_a_0;
    wire is_nan_a_2 = 0b0;
    wire is_nan_a_3 = mant_a != is_nan_a_2;
    wire is_nan_a_4 = is_nan_a_1 && is_nan_a_3;
    assign is_nan_a = is_nan_a_4;

    wire effective_subtraction_0 = sign_a != sign_b;
    assign effective_subtraction = effective_subtraction_0;

    wire small_add_0 = 0x00;
    wire small_add_1 = exp_a == small_add_0;
    wire small_add_2 = 0x00;
    wire small_add_3 = exp_b == small_add_2;
    wire small_add_4 = small_add_1 && small_add_3;
    assign small_add = small_add_4;

    wire is_normal_b_0 = 0b0;
    wire is_normal_b_1 = exp_b != is_normal_b_0;
    wire is_normal_b_2 = 0b0;
    wire is_normal_b_3 = mant_b != is_normal_b_2;
    wire is_normal_b_4 = is_normal_b_1 && is_normal_b_3;
    assign is_normal_b = is_normal_b_4;

    wire is_subnormal_b_0 = 0b0;
    wire is_subnormal_b_1 = exp_b == is_subnormal_b_0;
    wire is_subnormal_b_2 = 0b0;
    wire is_subnormal_b_3 = mant_b != is_subnormal_b_2;
    wire is_subnormal_b_4 = is_subnormal_b_1 && is_subnormal_b_3;
    assign is_subnormal_b = is_subnormal_b_4;

    wire is_zero_b_0 = 0b0;
    wire is_zero_b_1 = exp_b == is_zero_b_0;
    wire is_zero_b_2 = 0b0;
    wire is_zero_b_3 = mant_b == is_zero_b_2;
    wire is_zero_b_4 = is_zero_b_1 && is_zero_b_3;
    assign is_zero_b = is_zero_b_4;

    wire is_inf_b_0 = 0xFF;
    wire is_inf_b_1 = exp_b == is_inf_b_0;
    wire is_inf_b_2 = 0b0;
    wire is_inf_b_3 = mant_b == is_inf_b_2;
    wire is_inf_b_4 = is_inf_b_1 && is_inf_b_3;
    assign is_inf_b = is_inf_b_4;

    wire is_nan_b_0 = 0xFF;
    wire is_nan_b_1 = exp_b == is_nan_b_0;
    wire is_nan_b_2 = 0b0;
    wire is_nan_b_3 = mant_b != is_nan_b_2;
    wire is_nan_b_4 = is_nan_b_1 && is_nan_b_3;
    assign is_nan_b = is_nan_b_4;

    wire is_opposite_0 = sign_a != sign_b;
    wire is_opposite_1 = exp_a == exp_b;
    wire is_opposite_2 = is_opposite_0 && is_opposite_1;
    wire is_opposite_3 = mant_a == mant_b;
    wire is_opposite_4 = is_opposite_2 && is_opposite_3;
    assign is_opposite = is_opposite_4;

    wire mant_ext_a_0 = 0b0;
    wire mant_ext_a_1 = {p[2]["name"]};
    wire mant_ext_a_2 = 0b1;
    wire mant_ext_a_3 = {p[2]["name"]};
    wire mant_ext_a_4 = is_subnormal_a? mant_ext_a_1 : mant_ext_a_3;
    assign mant_ext_a = mant_ext_a_4;

    wire exp_ext_a_0 = 1;
    wire exp_ext_a_1 = exp_a + exp_ext_a_0;
    wire exp_ext_a_2 = is_subnormal_a? exp_ext_a_1 : exp_a;
    assign exp_ext_a = exp_ext_a_2;

    wire result_sign_one_zero_0 = is_zero_a? sign_b : sign_a;
    assign result_sign_one_zero = result_sign_one_zero_0;

    wire result_exp_one_zero_0 = is_zero_a? exp_b : exp_a;
    assign result_exp_one_zero = result_exp_one_zero_0;

    wire result_mant_one_zero_0 = is_zero_a? mant_b : mant_a;
    assign result_mant_one_zero = result_mant_one_zero_0;

    wire result_sign_inf_0 = is_inf_a? sign_a : sign_b;
    assign result_sign_inf = result_sign_inf_0;

    wire is_Snan_a_0 = io_a[22];
    wire is_Snan_a_1 = !is_Snan_a_0;
    wire is_Snan_a_2 = is_nan_a && is_Snan_a_1;
    assign is_Snan_a = is_Snan_a_2;

    wire mant_ext_b_0 = 0b0;
    wire mant_ext_b_1 = {p[2]["name"]};
    wire mant_ext_b_2 = 0b1;
    wire mant_ext_b_3 = {p[2]["name"]};
    wire mant_ext_b_4 = is_subnormal_b? mant_ext_b_1 : mant_ext_b_3;
    assign mant_ext_b = mant_ext_b_4;

    wire exp_ext_b_0 = 1;
    wire exp_ext_b_1 = exp_b + exp_ext_b_0;
    wire exp_ext_b_2 = is_subnormal_b? exp_ext_b_1 : exp_b;
    assign exp_ext_b = exp_ext_b_2;

    wire is_both_zero_0 = is_zero_a && is_zero_b;
    wire is_both_zero_1 = sign_a == sign_b;
    wire is_both_zero_2 = is_both_zero_0 && is_both_zero_1;
    assign is_both_zero = is_both_zero_2;

    wire is_Snan_b_0 = io_b[22];
    wire is_Snan_b_1 = !is_Snan_b_0;
    wire is_Snan_b_2 = is_nan_b && is_Snan_b_1;
    assign is_Snan_b = is_Snan_b_2;

    wire is_nan_0 = is_nan_a || is_nan_b;
    wire is_nan_1 = is_inf_a && is_inf_b;
    wire is_nan_2 = sign_a != sign_b;
    wire is_nan_3 = is_nan_1 && is_nan_2;
    wire is_nan_4 = is_nan_0 || is_nan_3;
    assign is_nan = is_nan_4;

    wire exp_diff_0 = exp_ext_a > exp_ext_b;
    wire exp_diff_1 = exp_ext_a - exp_ext_b;
    wire exp_diff_2 = exp_ext_b - exp_ext_a;
    wire exp_diff_3 = exp_diff_0? exp_diff_1 : exp_diff_2;
    assign exp_diff = exp_diff_3;

    wire aligned_exp_0 = exp_ext_a > exp_ext_b;
    wire aligned_exp_1 = aligned_exp_0? exp_ext_a : exp_ext_b;
    assign aligned_exp = aligned_exp_1;

    wire need_swap_0 = exp_ext_a < exp_ext_b;
    wire need_swap_1 = exp_ext_a == exp_ext_b;
    wire need_swap_2 = mant_ext_a < mant_ext_b;
    wire need_swap_3 = need_swap_1 && need_swap_2;
    wire need_swap_4 = need_swap_0 || need_swap_3;
    assign need_swap = need_swap_4;

    wire is_one_zero_0 = is_zero_a || is_zero_b;
    wire is_one_zero_1 = !is_both_zero;
    wire is_one_zero_2 = is_one_zero_0 && is_one_zero_1;
    assign is_one_zero = is_one_zero_2;

    wire special_flag_0 = is_Snan_a || is_Snan_b;
    wire special_flag_1 = is_inf_a && is_inf_b;
    wire special_flag_2 = sign_a != sign_b;
    wire special_flag_3 = special_flag_1 && special_flag_2;
    wire special_flag_4 = special_flag_0 || special_flag_3;
    assign special_flag = special_flag_4;

    wire is_inf_0 = is_inf_a || is_inf_b;
    wire is_inf_1 = !is_nan;
    wire is_inf_2 = is_inf_0 && is_inf_1;
    assign is_inf = is_inf_2;

    wire shift_too_large_0 = 26;
    wire shift_too_large_1 = exp_diff >= shift_too_large_0;
    assign shift_too_large = shift_too_large_1;

    wire shift_smaller_0 = 0b00;
    wire shift_smaller_1 = {p[2]["name"]};
    wire shift_smaller_2 = 0b00;
    wire shift_smaller_3 = {p[2]["name"]};
    wire shift_smaller_4 = need_swap? shift_smaller_1 : shift_smaller_3;
    assign shift_smaller = shift_smaller_4;

    wire aligned_mant_larger_0 = 0b0;
    wire aligned_mant_larger_1 = 0b000;
    wire aligned_mant_larger_2 = {p[2]["name"]};
    wire aligned_mant_larger_3 = 0b0;
    wire aligned_mant_larger_4 = 0b000;
    wire aligned_mant_larger_5 = {p[2]["name"]};
    wire aligned_mant_larger_6 = need_swap? aligned_mant_larger_2 : aligned_mant_larger_5;
    assign aligned_mant_larger = aligned_mant_larger_6;

    wire resultant_sign_0 = !effective_subtraction;
    wire resultant_sign_1 = need_swap? sign_b : sign_a;
    wire resultant_sign_2 = resultant_sign_0? sign_a : resultant_sign_1;
    assign resultant_sign = resultant_sign_2;

    wire special_result_0 = {p[2]["name"]};
    wire special_result_1 = {p[2]["name"]};
    wire special_result_2 = {p[2]["name"]};
    wire special_result_3 = {p[2]["name"]};
    wire special_result_4 = {p[2]["name"]};
    wire special_result_5 = 0b0;
    wire special_result_6 = 0xFF;
    wire special_result_7 = 0b10000000000000000000000;
    wire special_result_8 = {p[2]["name"]};
    wire special_result_9 = is_one_zero? special_result_4 : special_result_8;
    wire special_result_10 = is_opposite? special_result_3 : special_result_9;
    wire special_result_11 = is_both_zero? special_result_2 : special_result_10;
    wire special_result_12 = is_inf? special_result_1 : special_result_11;
    wire special_result_13 = is_nan? special_result_0 : special_result_12;
    assign special_result = special_result_13;

    wire special_case_happen_0 = is_nan || is_inf;
    wire special_case_happen_1 = special_case_happen_0 || is_both_zero;
    wire special_case_happen_2 = special_case_happen_1 || is_opposite;
    wire special_case_happen_3 = special_case_happen_2 || is_one_zero;
    assign special_case_happen = special_case_happen_3;

    wire main_0 = 0;
    wire main_1 = shift_smaller >> exp_diff;
    wire main_2 = shift_too_large? main_0 : main_1;
    assign main = main_2;

    wire smaller_sticky_0 = |shift_smaller;
    wire smaller_sticky_1 = 1;
    wire smaller_sticky_2 = smaller_sticky_1 << exp_diff;
    wire smaller_sticky_3 = 1;
    wire smaller_sticky_4 = smaller_sticky_2 - smaller_sticky_3;
    wire smaller_sticky_5 = shift_smaller & smaller_sticky_4;
    wire smaller_sticky_6 = |smaller_sticky_5;
    wire smaller_sticky_7 = shift_too_large? smaller_sticky_0 : smaller_sticky_6;
    assign smaller_sticky = smaller_sticky_7;

    wire rmin_0 = 0b001;
    wire rmin_1 = io_rm == rmin_0;
    wire rmin_2 = 0b010;
    wire rmin_3 = io_rm == rmin_2;
    wire rmin_4 = !resultant_sign;
    wire rmin_5 = rmin_3 && rmin_4;
    wire rmin_6 = rmin_1 || rmin_5;
    wire rmin_7 = 0b011;
    wire rmin_8 = io_rm == rmin_7;
    wire rmin_9 = rmin_8 && resultant_sign;
    wire rmin_10 = rmin_6 || rmin_9;
    assign rmin = rmin_10;

    wire aligned_mant_smaller_0 = 0b0;
    wire aligned_mant_smaller_1 = {p[2]["name"]};
    assign aligned_mant_smaller = aligned_mant_smaller_1;

    wire overflow_result_0 = 0xFE;
    wire overflow_result_1 = 0xFF;
    wire overflow_result_2 = rmin? overflow_result_0 : overflow_result_1;
    wire overflow_result_3 = 0x7FFFFF;
    wire overflow_result_4 = 0b0;
    wire overflow_result_5 = rmin? overflow_result_3 : overflow_result_4;
    wire overflow_result_6 = {p[2]["name"]};
    assign overflow_result = overflow_result_6;

    wire adder_result_0 = !effective_subtraction;
    wire adder_result_1 = aligned_mant_larger + aligned_mant_smaller;
    wire adder_result_2 = aligned_mant_larger - aligned_mant_smaller;
    wire adder_result_3 = adder_result_0? adder_result_1 : adder_result_2;
    assign adder_result = adder_result_3;

    wire carry_out_0 = adder_result[27];
    assign carry_out = carry_out_0;

    wire implied_bit_0 = adder_result[26];
    assign implied_bit = implied_bit_0;

    wire computed_shift_0 = adder_result[25];
    wire computed_shift_1 = 1;
    wire computed_shift_2 = adder_result[24];
    wire computed_shift_3 = 2;
    wire computed_shift_4 = adder_result[23];
    wire computed_shift_5 = 3;
    wire computed_shift_6 = adder_result[22];
    wire computed_shift_7 = 4;
    wire computed_shift_8 = adder_result[21];
    wire computed_shift_9 = 5;
    wire computed_shift_10 = adder_result[20];
    wire computed_shift_11 = 6;
    wire computed_shift_12 = adder_result[19];
    wire computed_shift_13 = 7;
    wire computed_shift_14 = adder_result[18];
    wire computed_shift_15 = 8;
    wire computed_shift_16 = adder_result[17];
    wire computed_shift_17 = 9;
    wire computed_shift_18 = adder_result[16];
    wire computed_shift_19 = 10;
    wire computed_shift_20 = adder_result[15];
    wire computed_shift_21 = 11;
    wire computed_shift_22 = adder_result[14];
    wire computed_shift_23 = 12;
    wire computed_shift_24 = adder_result[13];
    wire computed_shift_25 = 13;
    wire computed_shift_26 = adder_result[12];
    wire computed_shift_27 = 14;
    wire computed_shift_28 = adder_result[11];
    wire computed_shift_29 = 15;
    wire computed_shift_30 = adder_result[10];
    wire computed_shift_31 = 16;
    wire computed_shift_32 = adder_result[9];
    wire computed_shift_33 = 17;
    wire computed_shift_34 = adder_result[8];
    wire computed_shift_35 = 18;
    wire computed_shift_36 = adder_result[7];
    wire computed_shift_37 = 19;
    wire computed_shift_38 = adder_result[6];
    wire computed_shift_39 = 20;
    wire computed_shift_40 = adder_result[5];
    wire computed_shift_41 = 21;
    wire computed_shift_42 = adder_result[4];
    wire computed_shift_43 = 22;
    wire computed_shift_44 = adder_result[3];
    wire computed_shift_45 = 23;
    wire computed_shift_46 = 24;
    wire computed_shift_47 = computed_shift_44? computed_shift_45 : computed_shift_46;
    wire computed_shift_48 = computed_shift_42? computed_shift_43 : computed_shift_47;
    wire computed_shift_49 = computed_shift_40? computed_shift_41 : computed_shift_48;
    wire computed_shift_50 = computed_shift_38? computed_shift_39 : computed_shift_49;
    wire computed_shift_51 = computed_shift_36? computed_shift_37 : computed_shift_50;
    wire computed_shift_52 = computed_shift_34? computed_shift_35 : computed_shift_51;
    wire computed_shift_53 = computed_shift_32? computed_shift_33 : computed_shift_52;
    wire computed_shift_54 = computed_shift_30? computed_shift_31 : computed_shift_53;
    wire computed_shift_55 = computed_shift_28? computed_shift_29 : computed_shift_54;
    wire computed_shift_56 = computed_shift_26? computed_shift_27 : computed_shift_55;
    wire computed_shift_57 = computed_shift_24? computed_shift_25 : computed_shift_56;
    wire computed_shift_58 = computed_shift_22? computed_shift_23 : computed_shift_57;
    wire computed_shift_59 = computed_shift_20? computed_shift_21 : computed_shift_58;
    wire computed_shift_60 = computed_shift_18? computed_shift_19 : computed_shift_59;
    wire computed_shift_61 = computed_shift_16? computed_shift_17 : computed_shift_60;
    wire computed_shift_62 = computed_shift_14? computed_shift_15 : computed_shift_61;
    wire computed_shift_63 = computed_shift_12? computed_shift_13 : computed_shift_62;
    wire computed_shift_64 = computed_shift_10? computed_shift_11 : computed_shift_63;
    wire computed_shift_65 = computed_shift_8? computed_shift_9 : computed_shift_64;
    wire computed_shift_66 = computed_shift_6? computed_shift_7 : computed_shift_65;
    wire computed_shift_67 = computed_shift_4? computed_shift_5 : computed_shift_66;
    wire computed_shift_68 = computed_shift_2? computed_shift_3 : computed_shift_67;
    wire computed_shift_69 = computed_shift_0? computed_shift_1 : computed_shift_68;
    assign computed_shift = computed_shift_69;

    wire cancellation_0 = !carry_out;
    wire cancellation_1 = !implied_bit;
    wire cancellation_2 = cancellation_0 && cancellation_1;
    assign cancellation = cancellation_2;

    wire keep_0 = !carry_out;
    wire keep_1 = keep_0 && implied_bit;
    assign keep = keep_1;

    wire real_shift_norm_0 = aligned_exp > computed_shift;
    wire real_shift_norm_1 = 1;
    wire real_shift_norm_2 = aligned_exp - real_shift_norm_1;
    wire real_shift_norm_3 = real_shift_norm_0? computed_shift : real_shift_norm_2;
    assign real_shift_norm = real_shift_norm_3;

    wire adjusted_exp_0 = aligned_exp > computed_shift;
    wire adjusted_exp_1 = aligned_exp - computed_shift;
    wire adjusted_exp_2 = 0b0;
    wire adjusted_exp_3 = adjusted_exp_0? adjusted_exp_1 : adjusted_exp_2;
    assign adjusted_exp = adjusted_exp_3;

    wire normalized_mantissa_0 = adder_result[27: 2];
    wire normalized_mantissa_1 = adder_result[1: 0];
    wire normalized_mantissa_2 = |normalized_mantissa_1;
    wire normalized_mantissa_3 = {p[2]["name"]};
    wire normalized_mantissa_4 = keep || small_add;
    wire normalized_mantissa_5 = adder_result[26: 1];
    wire normalized_mantissa_6 = adder_result[0];
    wire normalized_mantissa_7 = {p[2]["name"]};
    wire normalized_mantissa_8 = !small_add;
    wire normalized_mantissa_9 = cancellation && normalized_mantissa_8;
    wire normalized_mantissa_10 = adder_result[25: 0];
    wire normalized_mantissa_11 = normalized_mantissa_10 << real_shift_norm;
    wire normalized_mantissa_12 = {p[2]["name"]};
    wire normalized_mantissa_13 = adder_result[26: 0];
    wire normalized_mantissa_14 = normalized_mantissa_9? normalized_mantissa_12 : normalized_mantissa_13;
    wire normalized_mantissa_15 = normalized_mantissa_4? normalized_mantissa_7 : normalized_mantissa_14;
    wire normalized_mantissa_16 = carry_out? normalized_mantissa_3 : normalized_mantissa_15;
    assign normalized_mantissa = normalized_mantissa_16;

    wire normalized_exp_0 = 1;
    wire normalized_exp_1 = aligned_exp + normalized_exp_0;
    wire normalized_exp_2 = cancellation? adjusted_exp : aligned_exp;
    wire normalized_exp_3 = keep? aligned_exp : normalized_exp_2;
    wire normalized_exp_4 = carry_out? normalized_exp_1 : normalized_exp_3;
    assign normalized_exp = normalized_exp_4;

    wire rounding_input_0 = normalized_mantissa[25: 3];
    assign rounding_input = rounding_input_0;

    wire f1_0 = normalized_mantissa[3];
    assign f1 = f1_0;

    wire f2_0 = normalized_mantissa[2];
    assign f2 = f2_0;

    wire f3_0 = normalized_mantissa[1: 0];
    wire f3_1 = |f3_0;
    assign f3 = f3_1;

    wire inexact_flag_0 = f2 | f3;
    assign inexact_flag = inexact_flag_0;

    wire round_up_0 = 0b000;
    wire round_up_1 = io_rm == round_up_0;
    wire round_up_2 = f1 || f3;
    wire round_up_3 = f2 && round_up_2;
    wire round_up_4 = 0b001;
    wire round_up_5 = io_rm == round_up_4;
    wire round_up_6 = 0b0;
    wire round_up_7 = 0b010;
    wire round_up_8 = io_rm == round_up_7;
    wire round_up_9 = inexact_flag && resultant_sign;
    wire round_up_10 = 0b011;
    wire round_up_11 = io_rm == round_up_10;
    wire round_up_12 = !resultant_sign;
    wire round_up_13 = inexact_flag && round_up_12;
    wire round_up_14 = 0b100;
    wire round_up_15 = io_rm == round_up_14;
    wire round_up_16 = 0b0;
    wire round_up_17 = round_up_15? f2 : round_up_16;
    wire round_up_18 = round_up_11? round_up_13 : round_up_17;
    wire round_up_19 = round_up_8? round_up_9 : round_up_18;
    wire round_up_20 = round_up_5? round_up_6 : round_up_19;
    wire round_up_21 = round_up_1? round_up_3 : round_up_20;
    assign round_up = round_up_21;

    wire n_carry_out_0 = &rounding_input;
    wire n_carry_out_1 = round_up && n_carry_out_0;
    assign n_carry_out = n_carry_out_1;

    wire rounded_mantissa_0 = 1;
    wire rounded_mantissa_1 = rounding_input + rounded_mantissa_0;
    wire rounded_mantissa_2 = round_up? rounded_mantissa_1 : rounding_input;
    assign rounded_mantissa = rounded_mantissa_2;

    wire rounded_exp_0 = n_carry_out + normalized_exp;
    assign rounded_exp = rounded_exp_0;

    wire tiny_0 = !n_carry_out;
    wire tiny_1 = keep && tiny_0;
    wire tiny_2 = cancellation || tiny_1;
    wire tiny_3 = small_add && tiny_2;
    assign tiny = tiny_3;

    wire overflow_0 = 0xFF;
    wire overflow_1 = rounded_exp == overflow_0;
    wire overflow_2 = 0xFE;
    wire overflow_3 = aligned_exp == overflow_2;
    wire overflow_4 = overflow_3 && carry_out;
    wire overflow_5 = overflow_1 || overflow_4;
    assign overflow = overflow_5;

    wire normal_result_0 = {p[2]["name"]};
    assign normal_result = normal_result_0;

    wire inexact_0 = inexact_flag || overflow;
    assign inexact = inexact_0;

    wire io_result_0 = overflow? overflow_result : normal_result;
    wire io_result_1 = special_case_happen? special_result : io_result_0;
    assign io_result = io_result_1;

    wire underflow_0 = tiny && inexact;
    wire underflow_1 = !overflow;
    wire underflow_2 = underflow_0 && underflow_1;
    assign underflow = underflow_2;

    wire io_fflags_0 = is_nan || is_inf;
    wire io_fflags_1 = 0b0;
    wire io_fflags_2 = {p[2]["name"]};
    wire io_fflags_3 = is_both_zero || is_opposite;
    wire io_fflags_4 = io_fflags_3 || is_one_zero;
    wire io_fflags_5 = 0b0;
    wire io_fflags_6 = {p[2]["name"]};
    wire io_fflags_7 = 0b0;
    wire io_fflags_8 = 0b0;
    wire io_fflags_9 = {p[2]["name"]};
    wire io_fflags_10 = io_fflags_4? io_fflags_6 : io_fflags_9;
    wire io_fflags_11 = io_fflags_0? io_fflags_2 : io_fflags_10;
    assign io_fflags = io_fflags_11;


endmodule