//golden
module FADD(
  input  [31:0] io_a,
  input  [31:0] io_b,
  input  [2:0]  io_rm,
  output [31:0] io_result,
  output [4:0]  io_fflags
);

  // Sub-module 1: Component Extraction
  wire sign_a = io_a[31];
  wire sign_b = io_b[31];
  wire [7:0] exp_a = io_a[30:23];
  wire [7:0] exp_b = io_b[30:23];
  wire [22:0] mant_a = io_a[22:0];
  wire [22:0] mant_b = io_b[22:0];

  // Sub-module 2: Classification of Operands
  wire is_normal_a = (exp_a != 8'b0) && (mant_a != 23'b0);
  wire is_normal_b = (exp_b != 8'b0) && (mant_b != 23'b0);
  wire is_subnormal_a = (exp_a == 8'b0) && (mant_a != 23'b0);
  wire is_subnormal_b = (exp_b == 8'b0) && (mant_b != 23'b0);
  wire is_zero_a = (exp_a == 8'b0) && (mant_a == 23'b0);
  wire is_zero_b = (exp_b == 8'b0) && (mant_b == 23'b0);
  wire is_inf_a = (exp_a == 8'hFF) && (mant_a == 23'b0);
  wire is_inf_b = (exp_b == 8'hFF) && (mant_b == 23'b0);
  wire is_nan_a = (exp_a == 8'hFF) && (mant_a != 23'b0);
  wire is_nan_b = (exp_b == 8'hFF) && (mant_b != 23'b0);
  wire is_Snan_a = (is_nan_a) && (!io_a[22]);
  wire is_Snan_b = (is_nan_b) && (!io_b[22]);


  // Sub-module 3: Handling Special Cases
  wire is_nan = is_nan_a || is_nan_b || (is_inf_a && is_inf_b && (sign_a != sign_b));
  wire is_inf = (is_inf_a || is_inf_b) && !is_nan;
  wire is_both_zero = is_zero_a && is_zero_b && (sign_a == sign_b);
  wire is_opposite = (sign_a != sign_b) && (exp_a == exp_b) && (mant_a == mant_b);
  wire is_one_zero = (is_zero_a || is_zero_b) && !is_both_zero;

  wire result_sign_nan = 1'b0;
  wire [7:0] result_exp_nan = 8'hFF;
  wire [22:0] result_mant_nan = 23'b10000000000000000000000;

  wire result_sign_inf = is_inf_a ? sign_a : sign_b;
  wire [7:0] result_exp_inf = 8'hFF;
  wire [22:0] result_mant_inf = 23'b0;

  wire result_sign_both_zero = sign_a;
  wire [7:0] result_exp_both_zero = 8'b0;
  wire [22:0] result_mant_both_zero = 23'b0;

  wire result_sign_opposite = (io_rm == 3'b010) ? 1'b1 : 1'b0;
  wire [7:0] result_exp_opposite = 8'b0;
  wire [22:0] result_mant_opposite = 23'b0;

  wire result_sign_one_zero = is_zero_a ? sign_b : sign_a;
  wire [7:0] result_exp_one_zero = is_zero_a ? exp_b : exp_a;
  wire [22:0] result_mant_one_zero = is_zero_a ? mant_b : mant_a;


  // Sub-module 4: Prepare for Addition
  wire effective_subtraction = (sign_a != sign_b);
  wire [23:0] mant_ext_a = is_subnormal_a? {1'b0, mant_a} : {1'b1, mant_a};
  wire [23:0] mant_ext_b = is_subnormal_b? {1'b0, mant_b} : {1'b1, mant_b};
  wire [7:0] exp_ext_a = is_subnormal_a ? (exp_a + 1) : exp_a;
  wire [7:0] exp_ext_b = is_subnormal_b ? (exp_b + 1) : exp_b;
  wire [7:0] exp_diff = (exp_ext_a > exp_ext_b) ? (exp_ext_a - exp_ext_b) : (exp_ext_b - exp_ext_a);
  wire [7:0] aligned_exp = (exp_ext_a > exp_ext_b) ? exp_ext_a : exp_ext_b;

  // Sub-module 5: Mantissa Alignment


  wire  need_swap = (exp_ext_a < exp_ext_b) || ((exp_ext_a == exp_ext_b) && (mant_ext_a < mant_ext_b));
  
  wire [25:0]  shift_smaller =  need_swap ? {mant_ext_a,2'b00} : {mant_ext_b,2'b00};
  wire  shift_too_large = (exp_diff >= 26);
  wire [25:0]  main =  shift_too_large ? 0 : ( shift_smaller >> exp_diff);
  wire   smaller_sticky =  shift_too_large ? | shift_smaller : |( shift_smaller & ((1 << exp_diff) - 1));

  wire [27:0]  aligned_mant_smaller =  {1'b0,  main,  smaller_sticky};
  wire [27:0]  aligned_mant_larger =  need_swap ? {1'b0, mant_ext_b,3'b000} : {1'b0, mant_ext_a,3'b000};

  wire  resultant_sign = (!effective_subtraction) ? sign_a : 
                    (need_swap) ? sign_b : sign_a;

  wire [27:0]  adder_result = !effective_subtraction ?  aligned_mant_larger +  aligned_mant_smaller : 
                                  aligned_mant_larger -  aligned_mant_smaller ;


  // Sub-module 6: Result Normalization and Left shifting
  wire carry_out = adder_result[27];
  wire implied_bit = adder_result[26];
  wire cancellation = !carry_out && !implied_bit;
  wire  keep = !carry_out && implied_bit;
  // wire small_add = is_subnormal_a && is_subnormal_b;
  wire small_add = (exp_a == 8'h00) && (exp_b == 8'h00);
  wire [4:0] computed_shift = 
    (adder_result[25]) ? 5'd1 :
    (adder_result[24]) ? 5'd2 :
    (adder_result[23]) ? 5'd3 :
    (adder_result[22]) ? 5'd4 :
    (adder_result[21]) ? 5'd5 :
    (adder_result[20]) ? 5'd6 :
    (adder_result[19]) ? 5'd7 :
    (adder_result[18]) ? 5'd8 :
    (adder_result[17]) ? 5'd9 :
    (adder_result[16]) ? 5'd10 :
    (adder_result[15]) ? 5'd11 :
    (adder_result[14]) ? 5'd12 :
    (adder_result[13]) ? 5'd13 :
    (adder_result[12]) ? 5'd14 :
    (adder_result[11]) ? 5'd15 :
    (adder_result[10]) ? 5'd16 :
    (adder_result[9]) ? 5'd17 :
    (adder_result[8]) ? 5'd18 :
    (adder_result[7]) ? 5'd19 :
    (adder_result[6]) ? 5'd20 :
    (adder_result[5]) ? 5'd21 :
    (adder_result[4]) ? 5'd22 :
    (adder_result[3]) ? 5'd23 :
    5'd24;
  wire [4:0] real_shift_norm = (aligned_exp > computed_shift) ? computed_shift : (aligned_exp - 1);
  wire [7:0] adjusted_exp = (aligned_exp > computed_shift) ? (aligned_exp - computed_shift) : 8'b0;
  
  wire [26:0]   normalized_mantissa =  carry_out ? { adder_result[27:2], | adder_result[1:0]} :
                          ( keep || small_add) ? { adder_result[26:1],  adder_result[0]} :
                          ( cancellation && !small_add) ? { adder_result[25:0] <<  real_shift_norm} :  adder_result[26:0] ;
  wire [7:0]   normalized_exp =  carry_out ? aligned_exp + 1 :
                                keep ? aligned_exp:
                                cancellation ?  adjusted_exp: aligned_exp;

  // Sub-module 7: Rounding processing
  wire [22:0] rounding_input = normalized_mantissa[25:3];
  wire f1 = normalized_mantissa[3];
  wire f2 = normalized_mantissa[2];
  wire f3 = | normalized_mantissa[1:0];
  wire inexact_flag = f2 | f3;
  wire round_up = 
    (io_rm == 3'b000) ? (f2 && (f1 || f3)) :
    (io_rm == 3'b001) ? 1'b0 :
    (io_rm == 3'b010) ? (inexact_flag && resultant_sign) :
    (io_rm == 3'b011) ? (inexact_flag && !resultant_sign) :
    (io_rm == 3'b100) ? f2 :
    1'b0;
  wire  n_carry_out =   round_up && & rounding_input;
  wire [7:0]  rounded_exp =  n_carry_out +   normalized_exp;
  wire [22:0]  rounded_mantissa =  round_up ?  rounding_input + 1 :  rounding_input;

  // Sub-module 8: Exception Flags
  wire tiny = small_add && (cancellation || (keep && !n_carry_out));
  wire overflow = (rounded_exp == 8'hFF) || ((aligned_exp == 8'hFE) && carry_out);
  wire inexact = inexact_flag || overflow;
  wire underflow = tiny && inexact && !overflow;
  wire special_flag = is_Snan_a || is_Snan_b || (is_inf_a && is_inf_b && (sign_a != sign_b));

  // Sub-module 9: Result Construction
  wire rmin = (io_rm == 3'b001) || ((io_rm == 3'b010) && !resultant_sign) || ((io_rm == 3'b011) && resultant_sign);
  wire [31:0] overflow_result = {resultant_sign, rmin ? 8'hFE : 8'hFF, rmin ? 23'h7FFFFF : 23'b0};
  wire [31:0] normal_result = {resultant_sign, rounded_exp, rounded_mantissa};
  wire [31:0] special_result = 
    is_nan ? {result_sign_nan, result_exp_nan, result_mant_nan} :
    is_inf ? {result_sign_inf, result_exp_inf, result_mant_inf} :
    is_both_zero ? {result_sign_both_zero, result_exp_both_zero, result_mant_both_zero} :
    is_opposite ? {result_sign_opposite, result_exp_opposite, result_mant_opposite} :
    is_one_zero? {result_sign_one_zero, result_exp_one_zero, result_mant_one_zero}:
    {1'b0, 8'hFF, 23'b10000000000000000000000};
  wire special_case_happen = is_nan || is_inf || is_both_zero || is_opposite || is_one_zero;
  
  assign io_fflags = (is_nan || is_inf) ? {special_flag, 4'b0} : (is_both_zero || is_opposite || is_one_zero) ? {5'b0}: {1'b0, 1'b0, overflow, underflow, inexact};
  assign io_result = special_case_happen ? special_result : (overflow ? overflow_result : normal_result);

endmodule
