package module;
import java.math.BigInteger;

public class FADD {
    // inputs
    private wire io_a = new wire(31, 0);
    private wire io_b = new wire(31, 0);
    private wire io_rm = new wire(2, 0);

    // outputs
    private wire io_result = new wire(31, 0);
    private wire io_fflags = new wire(4, 0);

    public void loadInput(BigInteger io_a, BigInteger io_b, BigInteger io_rm) {
        // load inputs
        this.io_a.set(io_a);
        this.io_b.set(io_b);
        this.io_rm.set(io_rm);
    }

    // getters
    public BigInteger get_io_result() {
        return this.io_result.get();
    }
    public BigInteger get_io_fflags() {
        return this.io_fflags.get();
    }

    public void compute() {
        // declare variables
        wire result_sign_nan = new wire(0, 0);
        wire result_exp_nan = new wire(7, 0);
        wire result_mant_nan = new wire(22, 0);
        wire result_exp_inf = new wire(7, 0);
        wire result_mant_inf = new wire(22, 0);
        wire result_exp_both_zero = new wire(7, 0);
        wire result_mant_both_zero = new wire(22, 0);
        wire result_exp_opposite = new wire(7, 0);
        wire result_mant_opposite = new wire(22, 0);
        wire sign_a = new wire(0, 0);
        wire exp_a = new wire(7, 0);
        wire mant_a = new wire(22, 0);
        wire sign_b = new wire(0, 0);
        wire exp_b = new wire(7, 0);
        wire mant_b = new wire(22, 0);
        wire result_sign_opposite = new wire(0, 0);
        wire result_sign_both_zero = new wire(0, 0);
        wire is_normal_a = new wire(0, 0);
        wire is_subnormal_a = new wire(0, 0);
        wire is_zero_a = new wire(0, 0);
        wire is_inf_a = new wire(0, 0);
        wire is_nan_a = new wire(0, 0);
        wire effective_subtraction = new wire(0, 0);
        wire small_add = new wire(0, 0);
        wire is_normal_b = new wire(0, 0);
        wire is_subnormal_b = new wire(0, 0);
        wire is_zero_b = new wire(0, 0);
        wire is_inf_b = new wire(0, 0);
        wire is_nan_b = new wire(0, 0);
        wire is_opposite = new wire(0, 0);
        wire mant_ext_a = new wire(23, 0);
        wire exp_ext_a = new wire(7, 0);
        wire result_sign_one_zero = new wire(0, 0);
        wire result_exp_one_zero = new wire(7, 0);
        wire result_mant_one_zero = new wire(22, 0);
        wire result_sign_inf = new wire(0, 0);
        wire is_Snan_a = new wire(0, 0);
        wire mant_ext_b = new wire(23, 0);
        wire exp_ext_b = new wire(7, 0);
        wire is_both_zero = new wire(0, 0);
        wire is_Snan_b = new wire(0, 0);
        wire is_nan = new wire(0, 0);
        wire exp_diff = new wire(7, 0);
        wire aligned_exp = new wire(7, 0);
        wire need_swap = new wire(0, 0);
        wire is_one_zero = new wire(0, 0);
        wire special_flag = new wire(0, 0);
        wire is_inf = new wire(0, 0);
        wire shift_too_large = new wire(0, 0);
        wire shift_smaller = new wire(25, 0);
        wire aligned_mant_larger = new wire(27, 0);
        wire resultant_sign = new wire(0, 0);
        wire special_result = new wire(31, 0);
        wire special_case_happen = new wire(0, 0);
        wire main = new wire(25, 0);
        wire smaller_sticky = new wire(0, 0);
        wire rmin = new wire(0, 0);
        wire aligned_mant_smaller = new wire(27, 0);
        wire overflow_result = new wire(31, 0);
        wire adder_result = new wire(27, 0);
        wire carry_out = new wire(0, 0);
        wire implied_bit = new wire(0, 0);
        wire computed_shift = new wire(4, 0);
        wire cancellation = new wire(0, 0);
        wire keep = new wire(0, 0);
        wire real_shift_norm = new wire(4, 0);
        wire adjusted_exp = new wire(7, 0);
        wire tiny = new wire(0, 0);
        wire normalized_mantissa = new wire(26, 0);
        wire normalized_exp = new wire(7, 0);
        wire rounding_input = new wire(22, 0);
        wire f1 = new wire(0, 0);
        wire f2 = new wire(0, 0);
        wire f3 = new wire(0, 0);
        wire rounded_exp = new wire(7, 0);
        wire inexact_flag = new wire(0, 0);
        wire overflow = new wire(0, 0);
        wire round_up = new wire(0, 0);
        wire inexact = new wire(0, 0);
        wire rounded_mantissa = new wire(22, 0);
        wire underflow = new wire(0, 0);
        wire normal_result = new wire(31, 0);

        // assignments
        wire result_sign_nan_0 = new wire(0, 0, 0b0);
        result_sign_nan.set(result_sign_nan_0);

        wire result_exp_nan_0 = new wire(7, 0, 0xFF);
        result_exp_nan.set(result_exp_nan_0);

        wire result_mant_nan_0 = new wire(22, 0, 0b10000000000000000000000);
        result_mant_nan.set(result_mant_nan_0);

        wire result_exp_inf_0 = new wire(7, 0, 0xFF);
        result_exp_inf.set(result_exp_inf_0);

        wire result_mant_inf_0 = new wire(22, 0, 0b0);
        result_mant_inf.set(result_mant_inf_0);

        wire result_exp_both_zero_0 = new wire(7, 0, 0b0);
        result_exp_both_zero.set(result_exp_both_zero_0);

        wire result_mant_both_zero_0 = new wire(22, 0, 0b0);
        result_mant_both_zero.set(result_mant_both_zero_0);

        wire result_exp_opposite_0 = new wire(7, 0, 0b0);
        result_exp_opposite.set(result_exp_opposite_0);

        wire result_mant_opposite_0 = new wire(22, 0, 0b0);
        result_mant_opposite.set(result_mant_opposite_0);

        wire sign_a_0 = io_a.getBit(31);
        sign_a.set(sign_a_0);

        wire exp_a_0 = io_a.getBits(30, 23);
        exp_a.set(exp_a_0);

        wire mant_a_0 = io_a.getBits(22, 0);
        mant_a.set(mant_a_0);

        wire sign_b_0 = io_b.getBit(31);
        sign_b.set(sign_b_0);

        wire exp_b_0 = io_b.getBits(30, 23);
        exp_b.set(exp_b_0);

        wire mant_b_0 = io_b.getBits(22, 0);
        mant_b.set(mant_b_0);

        wire result_sign_opposite_0 = new wire(2, 0, 0b010);
        wire result_sign_opposite_1 = io_rm.isEqual(result_sign_opposite_0);
        wire result_sign_opposite_2 = new wire(0, 0, 0b1);
        wire result_sign_opposite_3 = new wire(0, 0, 0b0);
        wire result_sign_opposite_4;
        if(result_sign_opposite_1.notZero())
            result_sign_opposite_4 = result_sign_opposite_2;
        else
            result_sign_opposite_4 = result_sign_opposite_3;
        result_sign_opposite.set(result_sign_opposite_4);

        result_sign_both_zero.set(sign_a);

        wire is_normal_a_0 = new wire(7, 0, 0b0);
        wire is_normal_a_1 = exp_a.notEqual(is_normal_a_0);
        wire is_normal_a_2 = new wire(22, 0, 0b0);
        wire is_normal_a_3 = mant_a.notEqual(is_normal_a_2);
        wire is_normal_a_4 = is_normal_a_1.logicalAnd(is_normal_a_3);
        is_normal_a.set(is_normal_a_4);

        wire is_subnormal_a_0 = new wire(7, 0, 0b0);
        wire is_subnormal_a_1 = exp_a.isEqual(is_subnormal_a_0);
        wire is_subnormal_a_2 = new wire(22, 0, 0b0);
        wire is_subnormal_a_3 = mant_a.notEqual(is_subnormal_a_2);
        wire is_subnormal_a_4 = is_subnormal_a_1.logicalAnd(is_subnormal_a_3);
        is_subnormal_a.set(is_subnormal_a_4);

        wire is_zero_a_0 = new wire(7, 0, 0b0);
        wire is_zero_a_1 = exp_a.isEqual(is_zero_a_0);
        wire is_zero_a_2 = new wire(22, 0, 0b0);
        wire is_zero_a_3 = mant_a.isEqual(is_zero_a_2);
        wire is_zero_a_4 = is_zero_a_1.logicalAnd(is_zero_a_3);
        is_zero_a.set(is_zero_a_4);

        wire is_inf_a_0 = new wire(7, 0, 0xFF);
        wire is_inf_a_1 = exp_a.isEqual(is_inf_a_0);
        wire is_inf_a_2 = new wire(22, 0, 0b0);
        wire is_inf_a_3 = mant_a.isEqual(is_inf_a_2);
        wire is_inf_a_4 = is_inf_a_1.logicalAnd(is_inf_a_3);
        is_inf_a.set(is_inf_a_4);

        wire is_nan_a_0 = new wire(7, 0, 0xFF);
        wire is_nan_a_1 = exp_a.isEqual(is_nan_a_0);
        wire is_nan_a_2 = new wire(22, 0, 0b0);
        wire is_nan_a_3 = mant_a.notEqual(is_nan_a_2);
        wire is_nan_a_4 = is_nan_a_1.logicalAnd(is_nan_a_3);
        is_nan_a.set(is_nan_a_4);

        wire effective_subtraction_0 = sign_a.notEqual(sign_b);
        effective_subtraction.set(effective_subtraction_0);

        wire small_add_0 = new wire(7, 0, 0x00);
        wire small_add_1 = exp_a.isEqual(small_add_0);
        wire small_add_2 = new wire(7, 0, 0x00);
        wire small_add_3 = exp_b.isEqual(small_add_2);
        wire small_add_4 = small_add_1.logicalAnd(small_add_3);
        small_add.set(small_add_4);

        wire is_normal_b_0 = new wire(7, 0, 0b0);
        wire is_normal_b_1 = exp_b.notEqual(is_normal_b_0);
        wire is_normal_b_2 = new wire(22, 0, 0b0);
        wire is_normal_b_3 = mant_b.notEqual(is_normal_b_2);
        wire is_normal_b_4 = is_normal_b_1.logicalAnd(is_normal_b_3);
        is_normal_b.set(is_normal_b_4);

        wire is_subnormal_b_0 = new wire(7, 0, 0b0);
        wire is_subnormal_b_1 = exp_b.isEqual(is_subnormal_b_0);
        wire is_subnormal_b_2 = new wire(22, 0, 0b0);
        wire is_subnormal_b_3 = mant_b.notEqual(is_subnormal_b_2);
        wire is_subnormal_b_4 = is_subnormal_b_1.logicalAnd(is_subnormal_b_3);
        is_subnormal_b.set(is_subnormal_b_4);

        wire is_zero_b_0 = new wire(7, 0, 0b0);
        wire is_zero_b_1 = exp_b.isEqual(is_zero_b_0);
        wire is_zero_b_2 = new wire(22, 0, 0b0);
        wire is_zero_b_3 = mant_b.isEqual(is_zero_b_2);
        wire is_zero_b_4 = is_zero_b_1.logicalAnd(is_zero_b_3);
        is_zero_b.set(is_zero_b_4);

        wire is_inf_b_0 = new wire(7, 0, 0xFF);
        wire is_inf_b_1 = exp_b.isEqual(is_inf_b_0);
        wire is_inf_b_2 = new wire(22, 0, 0b0);
        wire is_inf_b_3 = mant_b.isEqual(is_inf_b_2);
        wire is_inf_b_4 = is_inf_b_1.logicalAnd(is_inf_b_3);
        is_inf_b.set(is_inf_b_4);

        wire is_nan_b_0 = new wire(7, 0, 0xFF);
        wire is_nan_b_1 = exp_b.isEqual(is_nan_b_0);
        wire is_nan_b_2 = new wire(22, 0, 0b0);
        wire is_nan_b_3 = mant_b.notEqual(is_nan_b_2);
        wire is_nan_b_4 = is_nan_b_1.logicalAnd(is_nan_b_3);
        is_nan_b.set(is_nan_b_4);

        wire is_opposite_0 = sign_a.notEqual(sign_b);
        wire is_opposite_1 = exp_a.isEqual(exp_b);
        wire is_opposite_2 = is_opposite_0.logicalAnd(is_opposite_1);
        wire is_opposite_3 = mant_a.isEqual(mant_b);
        wire is_opposite_4 = is_opposite_2.logicalAnd(is_opposite_3);
        is_opposite.set(is_opposite_4);

        wire mant_ext_a_0 = new wire(0, 0, 0b0);
        wire mant_ext_a_1 = wire.concat(mant_ext_a_0, mant_a);
        wire mant_ext_a_2 = new wire(0, 0, 0b1);
        wire mant_ext_a_3 = wire.concat(mant_ext_a_2, mant_a);
        wire mant_ext_a_4;
        if(is_subnormal_a.notZero())
            mant_ext_a_4 = mant_ext_a_1;
        else
            mant_ext_a_4 = mant_ext_a_3;
        mant_ext_a.set(mant_ext_a_4);

        wire exp_ext_a_0 = new wire(0, 0, 1);
        wire exp_ext_a_1 = exp_a.add(exp_ext_a_0);
        wire exp_ext_a_2;
        if(is_subnormal_a.notZero())
            exp_ext_a_2 = exp_ext_a_1;
        else
            exp_ext_a_2 = exp_a;
        exp_ext_a.set(exp_ext_a_2);

        wire result_sign_one_zero_0;
        if(is_zero_a.notZero())
            result_sign_one_zero_0 = sign_b;
        else
            result_sign_one_zero_0 = sign_a;
        result_sign_one_zero.set(result_sign_one_zero_0);

        wire result_exp_one_zero_0;
        if(is_zero_a.notZero())
            result_exp_one_zero_0 = exp_b;
        else
            result_exp_one_zero_0 = exp_a;
        result_exp_one_zero.set(result_exp_one_zero_0);

        wire result_mant_one_zero_0;
        if(is_zero_a.notZero())
            result_mant_one_zero_0 = mant_b;
        else
            result_mant_one_zero_0 = mant_a;
        result_mant_one_zero.set(result_mant_one_zero_0);

        wire result_sign_inf_0;
        if(is_inf_a.notZero())
            result_sign_inf_0 = sign_a;
        else
            result_sign_inf_0 = sign_b;
        result_sign_inf.set(result_sign_inf_0);

        wire is_Snan_a_0 = io_a.getBit(22);
        wire is_Snan_a_1 = is_Snan_a_0.logicalNot();
        wire is_Snan_a_2 = is_nan_a.logicalAnd(is_Snan_a_1);
        is_Snan_a.set(is_Snan_a_2);

        wire mant_ext_b_0 = new wire(0, 0, 0b0);
        wire mant_ext_b_1 = wire.concat(mant_ext_b_0, mant_b);
        wire mant_ext_b_2 = new wire(0, 0, 0b1);
        wire mant_ext_b_3 = wire.concat(mant_ext_b_2, mant_b);
        wire mant_ext_b_4;
        if(is_subnormal_b.notZero())
            mant_ext_b_4 = mant_ext_b_1;
        else
            mant_ext_b_4 = mant_ext_b_3;
        mant_ext_b.set(mant_ext_b_4);

        wire exp_ext_b_0 = new wire(0, 0, 1);
        wire exp_ext_b_1 = exp_b.add(exp_ext_b_0);
        wire exp_ext_b_2;
        if(is_subnormal_b.notZero())
            exp_ext_b_2 = exp_ext_b_1;
        else
            exp_ext_b_2 = exp_b;
        exp_ext_b.set(exp_ext_b_2);

        wire is_both_zero_0 = is_zero_a.logicalAnd(is_zero_b);
        wire is_both_zero_1 = sign_a.isEqual(sign_b);
        wire is_both_zero_2 = is_both_zero_0.logicalAnd(is_both_zero_1);
        is_both_zero.set(is_both_zero_2);

        wire is_Snan_b_0 = io_b.getBit(22);
        wire is_Snan_b_1 = is_Snan_b_0.logicalNot();
        wire is_Snan_b_2 = is_nan_b.logicalAnd(is_Snan_b_1);
        is_Snan_b.set(is_Snan_b_2);

        wire is_nan_0 = is_nan_a.logicalOr(is_nan_b);
        wire is_nan_1 = is_inf_a.logicalAnd(is_inf_b);
        wire is_nan_2 = sign_a.notEqual(sign_b);
        wire is_nan_3 = is_nan_1.logicalAnd(is_nan_2);
        wire is_nan_4 = is_nan_0.logicalOr(is_nan_3);
        is_nan.set(is_nan_4);

        wire exp_diff_0 = exp_ext_a.greaterThan(exp_ext_b);
        wire exp_diff_1 = exp_ext_a.sub(exp_ext_b);
        wire exp_diff_2 = exp_ext_b.sub(exp_ext_a);
        wire exp_diff_3;
        if(exp_diff_0.notZero())
            exp_diff_3 = exp_diff_1;
        else
            exp_diff_3 = exp_diff_2;
        exp_diff.set(exp_diff_3);

        wire aligned_exp_0 = exp_ext_a.greaterThan(exp_ext_b);
        wire aligned_exp_1;
        if(aligned_exp_0.notZero())
            aligned_exp_1 = exp_ext_a;
        else
            aligned_exp_1 = exp_ext_b;
        aligned_exp.set(aligned_exp_1);

        wire need_swap_0 = exp_ext_a.lessThan(exp_ext_b);
        wire need_swap_1 = exp_ext_a.isEqual(exp_ext_b);
        wire need_swap_2 = mant_ext_a.lessThan(mant_ext_b);
        wire need_swap_3 = need_swap_1.logicalAnd(need_swap_2);
        wire need_swap_4 = need_swap_0.logicalOr(need_swap_3);
        need_swap.set(need_swap_4);

        wire is_one_zero_0 = is_zero_a.logicalOr(is_zero_b);
        wire is_one_zero_1 = is_both_zero.logicalNot();
        wire is_one_zero_2 = is_one_zero_0.logicalAnd(is_one_zero_1);
        is_one_zero.set(is_one_zero_2);

        wire special_flag_0 = is_Snan_a.logicalOr(is_Snan_b);
        wire special_flag_1 = is_inf_a.logicalAnd(is_inf_b);
        wire special_flag_2 = sign_a.notEqual(sign_b);
        wire special_flag_3 = special_flag_1.logicalAnd(special_flag_2);
        wire special_flag_4 = special_flag_0.logicalOr(special_flag_3);
        special_flag.set(special_flag_4);

        wire is_inf_0 = is_inf_a.logicalOr(is_inf_b);
        wire is_inf_1 = is_nan.logicalNot();
        wire is_inf_2 = is_inf_0.logicalAnd(is_inf_1);
        is_inf.set(is_inf_2);

        wire shift_too_large_0 = new wire(4, 0, 26);
        wire shift_too_large_1 = exp_diff.greaterEqual(shift_too_large_0);
        shift_too_large.set(shift_too_large_1);

        wire shift_smaller_0 = new wire(1, 0, 0b00);
        wire shift_smaller_1 = wire.concat(mant_ext_a, shift_smaller_0);
        wire shift_smaller_2 = new wire(1, 0, 0b00);
        wire shift_smaller_3 = wire.concat(mant_ext_b, shift_smaller_2);
        wire shift_smaller_4;
        if(need_swap.notZero())
            shift_smaller_4 = shift_smaller_1;
        else
            shift_smaller_4 = shift_smaller_3;
        shift_smaller.set(shift_smaller_4);

        wire aligned_mant_larger_0 = new wire(0, 0, 0b0);
        wire aligned_mant_larger_1 = new wire(2, 0, 0b000);
        wire aligned_mant_larger_2 = wire.concat(aligned_mant_larger_0, mant_ext_b, aligned_mant_larger_1);
        wire aligned_mant_larger_3 = new wire(0, 0, 0b0);
        wire aligned_mant_larger_4 = new wire(2, 0, 0b000);
        wire aligned_mant_larger_5 = wire.concat(aligned_mant_larger_3, mant_ext_a, aligned_mant_larger_4);
        wire aligned_mant_larger_6;
        if(need_swap.notZero())
            aligned_mant_larger_6 = aligned_mant_larger_2;
        else
            aligned_mant_larger_6 = aligned_mant_larger_5;
        aligned_mant_larger.set(aligned_mant_larger_6);

        wire resultant_sign_0 = effective_subtraction.logicalNot();
        wire resultant_sign_1;
        if(need_swap.notZero())
            resultant_sign_1 = sign_b;
        else
            resultant_sign_1 = sign_a;
        wire resultant_sign_2;
        if(resultant_sign_0.notZero())
            resultant_sign_2 = sign_a;
        else
            resultant_sign_2 = resultant_sign_1;
        resultant_sign.set(resultant_sign_2);

        wire special_result_0 = wire.concat(result_sign_nan, result_exp_nan, result_mant_nan);
        wire special_result_1 = wire.concat(result_sign_inf, result_exp_inf, result_mant_inf);
        wire special_result_2 = wire.concat(result_sign_both_zero, result_exp_both_zero, result_mant_both_zero);
        wire special_result_3 = wire.concat(result_sign_opposite, result_exp_opposite, result_mant_opposite);
        wire special_result_4 = wire.concat(result_sign_one_zero, result_exp_one_zero, result_mant_one_zero);
        wire special_result_5 = new wire(0, 0, 0b0);
        wire special_result_6 = new wire(7, 0, 0xFF);
        wire special_result_7 = new wire(22, 0, 0b10000000000000000000000);
        wire special_result_8 = wire.concat(special_result_5, special_result_6, special_result_7);
        wire special_result_9;
        if(is_one_zero.notZero())
            special_result_9 = special_result_4;
        else
            special_result_9 = special_result_8;
        wire special_result_10;
        if(is_opposite.notZero())
            special_result_10 = special_result_3;
        else
            special_result_10 = special_result_9;
        wire special_result_11;
        if(is_both_zero.notZero())
            special_result_11 = special_result_2;
        else
            special_result_11 = special_result_10;
        wire special_result_12;
        if(is_inf.notZero())
            special_result_12 = special_result_1;
        else
            special_result_12 = special_result_11;
        wire special_result_13;
        if(is_nan.notZero())
            special_result_13 = special_result_0;
        else
            special_result_13 = special_result_12;
        special_result.set(special_result_13);

        wire special_case_happen_0 = is_nan.logicalOr(is_inf);
        wire special_case_happen_1 = special_case_happen_0.logicalOr(is_both_zero);
        wire special_case_happen_2 = special_case_happen_1.logicalOr(is_opposite);
        wire special_case_happen_3 = special_case_happen_2.logicalOr(is_one_zero);
        special_case_happen.set(special_case_happen_3);

        wire main_0 = new wire(0, 0, 0);
        wire main_1 = shift_smaller.shiftRight(exp_diff);
        wire main_2;
        if(shift_too_large.notZero())
            main_2 = main_0;
        else
            main_2 = main_1;
        main.set(main_2);

        wire smaller_sticky_0 = shift_smaller.reduceOr();
        wire smaller_sticky_1 = new wire(0, 0, 1);
        wire smaller_sticky_2 = smaller_sticky_1.shiftLeft(exp_diff);
        wire smaller_sticky_3 = new wire(0, 0, 1);
        wire smaller_sticky_4 = smaller_sticky_2.sub(smaller_sticky_3);
        wire smaller_sticky_5 = shift_smaller.bitAnd(smaller_sticky_4);
        wire smaller_sticky_6 = smaller_sticky_5.reduceOr();
        wire smaller_sticky_7;
        if(shift_too_large.notZero())
            smaller_sticky_7 = smaller_sticky_0;
        else
            smaller_sticky_7 = smaller_sticky_6;
        smaller_sticky.set(smaller_sticky_7);

        wire rmin_0 = new wire(2, 0, 0b001);
        wire rmin_1 = io_rm.isEqual(rmin_0);
        wire rmin_2 = new wire(2, 0, 0b010);
        wire rmin_3 = io_rm.isEqual(rmin_2);
        wire rmin_4 = resultant_sign.logicalNot();
        wire rmin_5 = rmin_3.logicalAnd(rmin_4);
        wire rmin_6 = rmin_1.logicalOr(rmin_5);
        wire rmin_7 = new wire(2, 0, 0b011);
        wire rmin_8 = io_rm.isEqual(rmin_7);
        wire rmin_9 = rmin_8.logicalAnd(resultant_sign);
        wire rmin_10 = rmin_6.logicalOr(rmin_9);
        rmin.set(rmin_10);

        wire aligned_mant_smaller_0 = new wire(0, 0, 0b0);
        wire aligned_mant_smaller_1 = wire.concat(aligned_mant_smaller_0, main, smaller_sticky);
        aligned_mant_smaller.set(aligned_mant_smaller_1);

        wire overflow_result_0 = new wire(7, 0, 0xFE);
        wire overflow_result_1 = new wire(7, 0, 0xFF);
        wire overflow_result_2;
        if(rmin.notZero())
            overflow_result_2 = overflow_result_0;
        else
            overflow_result_2 = overflow_result_1;
        wire overflow_result_3 = new wire(22, 0, 0x7FFFFF);
        wire overflow_result_4 = new wire(22, 0, 0b0);
        wire overflow_result_5;
        if(rmin.notZero())
            overflow_result_5 = overflow_result_3;
        else
            overflow_result_5 = overflow_result_4;
        wire overflow_result_6 = wire.concat(resultant_sign, overflow_result_2, overflow_result_5);
        overflow_result.set(overflow_result_6);

        wire adder_result_0 = effective_subtraction.logicalNot();
        wire adder_result_1 = aligned_mant_larger.add(aligned_mant_smaller);
        wire adder_result_2 = aligned_mant_larger.sub(aligned_mant_smaller);
        wire adder_result_3;
        if(adder_result_0.notZero())
            adder_result_3 = adder_result_1;
        else
            adder_result_3 = adder_result_2;
        adder_result.set(adder_result_3);

        wire carry_out_0 = adder_result.getBit(27);
        carry_out.set(carry_out_0);

        wire implied_bit_0 = adder_result.getBit(26);
        implied_bit.set(implied_bit_0);

        wire computed_shift_0 = adder_result.getBit(25);
        wire computed_shift_1 = new wire(4, 0, 1);
        wire computed_shift_2 = adder_result.getBit(24);
        wire computed_shift_3 = new wire(4, 0, 2);
        wire computed_shift_4 = adder_result.getBit(23);
        wire computed_shift_5 = new wire(4, 0, 3);
        wire computed_shift_6 = adder_result.getBit(22);
        wire computed_shift_7 = new wire(4, 0, 4);
        wire computed_shift_8 = adder_result.getBit(21);
        wire computed_shift_9 = new wire(4, 0, 5);
        wire computed_shift_10 = adder_result.getBit(20);
        wire computed_shift_11 = new wire(4, 0, 6);
        wire computed_shift_12 = adder_result.getBit(19);
        wire computed_shift_13 = new wire(4, 0, 7);
        wire computed_shift_14 = adder_result.getBit(18);
        wire computed_shift_15 = new wire(4, 0, 8);
        wire computed_shift_16 = adder_result.getBit(17);
        wire computed_shift_17 = new wire(4, 0, 9);
        wire computed_shift_18 = adder_result.getBit(16);
        wire computed_shift_19 = new wire(4, 0, 10);
        wire computed_shift_20 = adder_result.getBit(15);
        wire computed_shift_21 = new wire(4, 0, 11);
        wire computed_shift_22 = adder_result.getBit(14);
        wire computed_shift_23 = new wire(4, 0, 12);
        wire computed_shift_24 = adder_result.getBit(13);
        wire computed_shift_25 = new wire(4, 0, 13);
        wire computed_shift_26 = adder_result.getBit(12);
        wire computed_shift_27 = new wire(4, 0, 14);
        wire computed_shift_28 = adder_result.getBit(11);
        wire computed_shift_29 = new wire(4, 0, 15);
        wire computed_shift_30 = adder_result.getBit(10);
        wire computed_shift_31 = new wire(4, 0, 16);
        wire computed_shift_32 = adder_result.getBit(9);
        wire computed_shift_33 = new wire(4, 0, 17);
        wire computed_shift_34 = adder_result.getBit(8);
        wire computed_shift_35 = new wire(4, 0, 18);
        wire computed_shift_36 = adder_result.getBit(7);
        wire computed_shift_37 = new wire(4, 0, 19);
        wire computed_shift_38 = adder_result.getBit(6);
        wire computed_shift_39 = new wire(4, 0, 20);
        wire computed_shift_40 = adder_result.getBit(5);
        wire computed_shift_41 = new wire(4, 0, 21);
        wire computed_shift_42 = adder_result.getBit(4);
        wire computed_shift_43 = new wire(4, 0, 22);
        wire computed_shift_44 = adder_result.getBit(3);
        wire computed_shift_45 = new wire(4, 0, 23);
        wire computed_shift_46 = new wire(4, 0, 24);
        wire computed_shift_47;
        if(computed_shift_44.notZero())
            computed_shift_47 = computed_shift_45;
        else
            computed_shift_47 = computed_shift_46;
        wire computed_shift_48;
        if(computed_shift_42.notZero())
            computed_shift_48 = computed_shift_43;
        else
            computed_shift_48 = computed_shift_47;
        wire computed_shift_49;
        if(computed_shift_40.notZero())
            computed_shift_49 = computed_shift_41;
        else
            computed_shift_49 = computed_shift_48;
        wire computed_shift_50;
        if(computed_shift_38.notZero())
            computed_shift_50 = computed_shift_39;
        else
            computed_shift_50 = computed_shift_49;
        wire computed_shift_51;
        if(computed_shift_36.notZero())
            computed_shift_51 = computed_shift_37;
        else
            computed_shift_51 = computed_shift_50;
        wire computed_shift_52;
        if(computed_shift_34.notZero())
            computed_shift_52 = computed_shift_35;
        else
            computed_shift_52 = computed_shift_51;
        wire computed_shift_53;
        if(computed_shift_32.notZero())
            computed_shift_53 = computed_shift_33;
        else
            computed_shift_53 = computed_shift_52;
        wire computed_shift_54;
        if(computed_shift_30.notZero())
            computed_shift_54 = computed_shift_31;
        else
            computed_shift_54 = computed_shift_53;
        wire computed_shift_55;
        if(computed_shift_28.notZero())
            computed_shift_55 = computed_shift_29;
        else
            computed_shift_55 = computed_shift_54;
        wire computed_shift_56;
        if(computed_shift_26.notZero())
            computed_shift_56 = computed_shift_27;
        else
            computed_shift_56 = computed_shift_55;
        wire computed_shift_57;
        if(computed_shift_24.notZero())
            computed_shift_57 = computed_shift_25;
        else
            computed_shift_57 = computed_shift_56;
        wire computed_shift_58;
        if(computed_shift_22.notZero())
            computed_shift_58 = computed_shift_23;
        else
            computed_shift_58 = computed_shift_57;
        wire computed_shift_59;
        if(computed_shift_20.notZero())
            computed_shift_59 = computed_shift_21;
        else
            computed_shift_59 = computed_shift_58;
        wire computed_shift_60;
        if(computed_shift_18.notZero())
            computed_shift_60 = computed_shift_19;
        else
            computed_shift_60 = computed_shift_59;
        wire computed_shift_61;
        if(computed_shift_16.notZero())
            computed_shift_61 = computed_shift_17;
        else
            computed_shift_61 = computed_shift_60;
        wire computed_shift_62;
        if(computed_shift_14.notZero())
            computed_shift_62 = computed_shift_15;
        else
            computed_shift_62 = computed_shift_61;
        wire computed_shift_63;
        if(computed_shift_12.notZero())
            computed_shift_63 = computed_shift_13;
        else
            computed_shift_63 = computed_shift_62;
        wire computed_shift_64;
        if(computed_shift_10.notZero())
            computed_shift_64 = computed_shift_11;
        else
            computed_shift_64 = computed_shift_63;
        wire computed_shift_65;
        if(computed_shift_8.notZero())
            computed_shift_65 = computed_shift_9;
        else
            computed_shift_65 = computed_shift_64;
        wire computed_shift_66;
        if(computed_shift_6.notZero())
            computed_shift_66 = computed_shift_7;
        else
            computed_shift_66 = computed_shift_65;
        wire computed_shift_67;
        if(computed_shift_4.notZero())
            computed_shift_67 = computed_shift_5;
        else
            computed_shift_67 = computed_shift_66;
        wire computed_shift_68;
        if(computed_shift_2.notZero())
            computed_shift_68 = computed_shift_3;
        else
            computed_shift_68 = computed_shift_67;
        wire computed_shift_69;
        if(computed_shift_0.notZero())
            computed_shift_69 = computed_shift_1;
        else
            computed_shift_69 = computed_shift_68;
        computed_shift.set(computed_shift_69);

        wire cancellation_0 = carry_out.logicalNot();
        wire cancellation_1 = implied_bit.logicalNot();
        wire cancellation_2 = cancellation_0.logicalAnd(cancellation_1);
        cancellation.set(cancellation_2);

        wire keep_0 = carry_out.logicalNot();
        wire keep_1 = keep_0.logicalAnd(implied_bit);
        keep.set(keep_1);

        wire real_shift_norm_0 = aligned_exp.greaterThan(computed_shift);
        wire real_shift_norm_1 = new wire(0, 0, 1);
        wire real_shift_norm_2 = aligned_exp.sub(real_shift_norm_1);
        wire real_shift_norm_3;
        if(real_shift_norm_0.notZero())
            real_shift_norm_3 = computed_shift;
        else
            real_shift_norm_3 = real_shift_norm_2;
        real_shift_norm.set(real_shift_norm_3);

        wire adjusted_exp_0 = aligned_exp.greaterThan(computed_shift);
        wire adjusted_exp_1 = aligned_exp.sub(computed_shift);
        wire adjusted_exp_2 = new wire(7, 0, 0b0);
        wire adjusted_exp_3;
        if(adjusted_exp_0.notZero())
            adjusted_exp_3 = adjusted_exp_1;
        else
            adjusted_exp_3 = adjusted_exp_2;
        adjusted_exp.set(adjusted_exp_3);

        wire tiny_0 = cancellation.logicalOr(keep);
        wire tiny_1 = small_add.logicalAnd(tiny_0);
        tiny.set(tiny_1);

        wire normalized_mantissa_0 = adder_result.getBits(27, 2);
        wire normalized_mantissa_1 = adder_result.getBits(1, 0);
        wire normalized_mantissa_2 = normalized_mantissa_1.reduceOr();
        wire normalized_mantissa_3 = wire.concat(normalized_mantissa_0, normalized_mantissa_2);
        wire normalized_mantissa_4 = keep.logicalOr(small_add);
        wire normalized_mantissa_5 = adder_result.getBits(26, 1);
        wire normalized_mantissa_6 = adder_result.getBit(0);
        wire normalized_mantissa_7 = wire.concat(normalized_mantissa_5, normalized_mantissa_6);
        wire normalized_mantissa_8 = small_add.logicalNot();
        wire normalized_mantissa_9 = cancellation.logicalAnd(normalized_mantissa_8);
        wire normalized_mantissa_10 = adder_result.getBits(25, 0);
        wire normalized_mantissa_11 = normalized_mantissa_10.shiftLeft(real_shift_norm);
        wire normalized_mantissa_12 = wire.concat(normalized_mantissa_11);
        wire normalized_mantissa_13 = adder_result.getBits(26, 0);
        wire normalized_mantissa_14;
        if(normalized_mantissa_9.notZero())
            normalized_mantissa_14 = normalized_mantissa_12;
        else
            normalized_mantissa_14 = normalized_mantissa_13;
        wire normalized_mantissa_15;
        if(normalized_mantissa_4.notZero())
            normalized_mantissa_15 = normalized_mantissa_7;
        else
            normalized_mantissa_15 = normalized_mantissa_14;
        wire normalized_mantissa_16;
        if(carry_out.notZero())
            normalized_mantissa_16 = normalized_mantissa_3;
        else
            normalized_mantissa_16 = normalized_mantissa_15;
        normalized_mantissa.set(normalized_mantissa_16);

        wire normalized_exp_0 = new wire(0, 0, 1);
        wire normalized_exp_1 = aligned_exp.add(normalized_exp_0);
        wire normalized_exp_2;
        if(cancellation.notZero())
            normalized_exp_2 = adjusted_exp;
        else
            normalized_exp_2 = aligned_exp;
        wire normalized_exp_3;
        if(keep.notZero())
            normalized_exp_3 = aligned_exp;
        else
            normalized_exp_3 = normalized_exp_2;
        wire normalized_exp_4;
        if(carry_out.notZero())
            normalized_exp_4 = normalized_exp_1;
        else
            normalized_exp_4 = normalized_exp_3;
        normalized_exp.set(normalized_exp_4);

        wire rounding_input_0 = normalized_mantissa.getBits(25, 3);
        rounding_input.set(rounding_input_0);

        wire f1_0 = normalized_mantissa.getBit(3);
        f1.set(f1_0);

        wire f2_0 = normalized_mantissa.getBit(2);
        f2.set(f2_0);

        wire f3_0 = normalized_mantissa.getBits(1, 0);
        wire f3_1 = f3_0.reduceOr();
        f3.set(f3_1);

        rounded_exp.set(normalized_exp);

        wire inexact_flag_0 = f2.bitOr(f3);
        inexact_flag.set(inexact_flag_0);

        wire overflow_0 = new wire(7, 0, 0xFF);
        wire overflow_1 = rounded_exp.isEqual(overflow_0);
        wire overflow_2 = new wire(7, 0, 0xFE);
        wire overflow_3 = aligned_exp.isEqual(overflow_2);
        wire overflow_4 = overflow_3.logicalAnd(carry_out);
        wire overflow_5 = overflow_1.logicalOr(overflow_4);
        overflow.set(overflow_5);

        wire round_up_0 = new wire(2, 0, 0b000);
        wire round_up_1 = io_rm.isEqual(round_up_0);
        wire round_up_2 = f1.logicalOr(f3);
        wire round_up_3 = f2.logicalAnd(round_up_2);
        wire round_up_4 = new wire(2, 0, 0b001);
        wire round_up_5 = io_rm.isEqual(round_up_4);
        wire round_up_6 = new wire(0, 0, 0b0);
        wire round_up_7 = new wire(2, 0, 0b010);
        wire round_up_8 = io_rm.isEqual(round_up_7);
        wire round_up_9 = inexact_flag.logicalAnd(resultant_sign);
        wire round_up_10 = new wire(2, 0, 0b011);
        wire round_up_11 = io_rm.isEqual(round_up_10);
        wire round_up_12 = resultant_sign.logicalNot();
        wire round_up_13 = inexact_flag.logicalAnd(round_up_12);
        wire round_up_14 = new wire(2, 0, 0b100);
        wire round_up_15 = io_rm.isEqual(round_up_14);
        wire round_up_16 = new wire(0, 0, 0b0);
        wire round_up_17;
        if(round_up_15.notZero())
            round_up_17 = f2;
        else
            round_up_17 = round_up_16;
        wire round_up_18;
        if(round_up_11.notZero())
            round_up_18 = round_up_13;
        else
            round_up_18 = round_up_17;
        wire round_up_19;
        if(round_up_8.notZero())
            round_up_19 = round_up_9;
        else
            round_up_19 = round_up_18;
        wire round_up_20;
        if(round_up_5.notZero())
            round_up_20 = round_up_6;
        else
            round_up_20 = round_up_19;
        wire round_up_21;
        if(round_up_1.notZero())
            round_up_21 = round_up_3;
        else
            round_up_21 = round_up_20;
        round_up.set(round_up_21);

        wire inexact_0 = inexact_flag.logicalOr(overflow);
        inexact.set(inexact_0);

        wire rounded_mantissa_0 = new wire(0, 0, 1);
        wire rounded_mantissa_1 = rounding_input.add(rounded_mantissa_0);
        wire rounded_mantissa_2;
        if(round_up.notZero())
            rounded_mantissa_2 = rounded_mantissa_1;
        else
            rounded_mantissa_2 = rounding_input;
        rounded_mantissa.set(rounded_mantissa_2);

        wire underflow_0 = tiny.logicalAnd(inexact);
        wire underflow_1 = overflow.logicalNot();
        wire underflow_2 = underflow_0.logicalAnd(underflow_1);
        underflow.set(underflow_2);

        wire normal_result_0 = wire.concat(resultant_sign, rounded_exp, rounded_mantissa);
        normal_result.set(normal_result_0);

        wire io_fflags_0 = is_nan.logicalOr(is_inf);
        wire io_fflags_1 = new wire(3, 0, 0b0);
        wire io_fflags_2 = wire.concat(special_flag, io_fflags_1);
        wire io_fflags_3 = is_both_zero.logicalOr(is_opposite);
        wire io_fflags_4 = io_fflags_3.logicalOr(is_one_zero);
        wire io_fflags_5 = new wire(4, 0, 0b0);
        wire io_fflags_6 = wire.concat(io_fflags_5);
        wire io_fflags_7 = new wire(0, 0, 0b0);
        wire io_fflags_8 = new wire(0, 0, 0b0);
        wire io_fflags_9 = wire.concat(io_fflags_7, io_fflags_8, overflow, underflow, inexact);
        wire io_fflags_10;
        if(io_fflags_4.notZero())
            io_fflags_10 = io_fflags_6;
        else
            io_fflags_10 = io_fflags_9;
        wire io_fflags_11;
        if(io_fflags_0.notZero())
            io_fflags_11 = io_fflags_2;
        else
            io_fflags_11 = io_fflags_10;
        io_fflags.set(io_fflags_11);

        wire io_result_0;
        if(overflow.notZero())
            io_result_0 = overflow_result;
        else
            io_result_0 = normal_result;
        wire io_result_1;
        if(special_case_happen.notZero())
            io_result_1 = special_result;
        else
            io_result_1 = io_result_0;
        io_result.set(io_result_1);

    }

}
