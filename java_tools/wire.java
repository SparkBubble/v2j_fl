package module;

import java.math.BigInteger;
import java.util.Arrays;

public class wire {
    private final int highBit;    // 最高位索引（包含）
    private final int lowBit;     // 最低位索引（包含）
    private final int bitWidth;   // 位宽 = high - low + 1
    private BigInteger value;


    private static boolean Debug = false;
    private static boolean Warning = false;

    static wire ZERO = new wire(0, 0, BigInteger.ZERO);
    static wire ONE = new wire(0, 0, BigInteger.ONE);

    // 构造函数（显式指定位域[high:low]）
    public wire(int highBit, int lowBit, BigInteger value) {
        if (highBit < lowBit) throw new IllegalArgumentException("Invalid bit range");
        this.highBit = highBit;
        this.lowBit = lowBit;
        this.bitWidth = highBit - lowBit + 1;
        this.value = truncate(value); // 截断到指定位宽
    }
    public wire(int highBit, int lowBit, long value) {
        this(highBit, lowBit, BigInteger.valueOf(value));
    }
    public wire(int highBit, int lowBit) {
        this(highBit, lowBit, BigInteger.ZERO);
    }
    // 隐式指定位宽
    public wire(BigInteger value) {
        this(value.equals(BigInteger.ZERO)? 0 : value.bitLength() - 1, 0, value);
    }
    public wire(long value) {
        this(BigInteger.valueOf(value));
    }

    // 截断值到当前位宽（无符号处理）
    private BigInteger truncate(BigInteger var, int n_bitWidth) {
        BigInteger nvar = var;
        while(nvar.compareTo(BigInteger.ZERO) < 0) {
            nvar = nvar.add(BigInteger.ONE.shiftLeft(n_bitWidth));
        }
        return var.and(BigInteger.ONE.shiftLeft(n_bitWidth).subtract(BigInteger.ONE));
    }
    private BigInteger truncate(BigInteger var) {
        return truncate(var, bitWidth);
    }
    
    // var[high:low]
    public wire getBits(int high, int low) {
        if (high < low || high > highBit || low < lowBit) 
            throw new IllegalArgumentException("Bit range out of bounds");
        
        int shift = low - lowBit;
        BigInteger mask = BigInteger.ONE.shiftLeft(high - low + 1).subtract(BigInteger.ONE);
        return new wire(high - low, 0, value.shiftRight(shift).and(mask));
    }

    // var[bit]
    public wire getBit(int bit) {
        if (bit < lowBit || bit > highBit)
            throw new IllegalArgumentException("Bit index out of bounds");
        return new wire(0, 0, value.testBit(bit - lowBit)? BigInteger.ONE : BigInteger.ZERO);
    }

    // var[high:low] = othervar
    public void setBits(int high, int low, wire other) {
        if (high < low || high > highBit || low < lowBit)
            throw new IllegalArgumentException("Bit range out of bounds");
        if (high - low + 1 < other.bitWidth){
            if (Debug)
                throw new IllegalArgumentException("Bit width mismatch. " + (high - low + 1) + " vs " + other.bitWidth);
            else if (Warning)
                System.err.println("Warning: Bit width mismatch. " + (high - low + 1) + " vs " + other.bitWidth);
        }
        BigInteger t_val = truncate(other.value, high - low + 1);

        BigInteger mask = BigInteger.ONE.shiftLeft(high - low + 1)
                .subtract(BigInteger.ONE).shiftLeft(low - lowBit);
        BigInteger cleared = value.andNot(mask);
        BigInteger newBits = t_val.shiftLeft(low - lowBit).and(mask);

        value = cleared.or(newBits);
    }

    // var[high:low] = imm
    public void setBits(int high, int low, BigInteger var) {
        this.setBits(high, low, new wire(var.bitLength() - 1, 0, var));
    }
    public void setBits(int high, int low, long var) {
        this.setBits(high, low, BigInteger.valueOf(var));
    }

    // var[bit] = othervar
    public void setBit(int bit, boolean var) {
        if (bit < lowBit || bit > highBit)
            throw new IllegalArgumentException("Bit index out of bounds");
        
        if (var)
            value.setBit(bit - lowBit);
        else
            value.clearBit(bit - lowBit);
    }
    public void setBit(int bit, wire other) {
        this.setBit(bit, !other.value.equals(BigInteger.ZERO));
    }
    // var[bit] = imm
    public void setBit(int bit, BigInteger var) {
        this.setBit(bit, !var.equals(BigInteger.ZERO));
    }
    public void setBit(int bit, long var) {
        this.setBit(bit, var != 0);
    }

    // var = othervar
    public void set(wire other) {
        if(bitWidth < other.bitWidth){
            if (Debug)
                throw new IllegalArgumentException("Bit width mismatch. " + bitWidth + " vs " + other.bitWidth);
            else if (Warning)
                System.err.println("Warning: Bit width mismatch. " + bitWidth + " vs " + other.bitWidth);
        }
        value = truncate(other.value);
    }

    // var = imm
    public void set(BigInteger var) {
        if(bitWidth < var.bitLength()){
            if (Debug)
                throw new IllegalArgumentException("Bit width mismatch. " + bitWidth + " vs " + var.bitLength());
            else if (Warning)
                System.err.println("Warning: Bit width mismatch. " + bitWidth + " vs " + var.bitLength());
        }
        value = truncate(var);
    }
    public void set(long var) {
        value = truncate(BigInteger.valueOf(var));
    }

    // {wire, wire, ...}
    public static wire concat(wire... wires) {
        int totalWidth = Arrays.stream(wires).mapToInt(w -> w.bitWidth).sum();
        BigInteger result = BigInteger.ZERO;
        int shift = 0;
        
        for (int i = wires.length - 1; i >= 0; i--) {
            wire w = wires[i];
            result = result.or(w.value.shiftLeft(shift));
            shift += w.bitWidth;
        }
        return new wire(totalWidth - 1, 0, result);
    }

    //-------------------------- 逻辑运算 --------------------------
    // &&
    public wire logicalAnd(wire other) {
        boolean res = !value.equals(BigInteger.ZERO) && !other.value.equals(BigInteger.ZERO);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // ||
    public wire logicalOr(wire other) {
        boolean res = !value.equals(BigInteger.ZERO) || !other.value.equals(BigInteger.ZERO);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // !
    public wire logicalNot() {
        boolean res = value.equals(BigInteger.ZERO);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    //-------------------------- 按位运算 --------------------------
    
    // &
    public wire bitAnd(wire other) {
        int maxwidth = Math.max(bitWidth, other.bitWidth);
        return new wire(maxwidth - 1, 0, value.and(other.value));
    }

    // |
    public wire bitOr(wire other) {
        int maxwidth = Math.max(bitWidth, other.bitWidth);
        return new wire(maxwidth - 1, 0, value.or(other.value));
    }

    // ^
    public wire bitXor(wire other) {
        int maxwidth = Math.max(bitWidth, other.bitWidth);
        return new wire(maxwidth - 1, 0, value.xor(other.value));
    }

    // ~
    public wire bitNot() {
        return new wire(bitWidth - 1, 0, value.xor(BigInteger.ONE.shiftLeft(bitWidth).subtract(BigInteger.ONE)));
    }

    //-------------------------- 算术运算 --------------------------


    // +
    public wire add(wire other) {
        return new wire(value.add(other.value));
    }

    // -
    public wire sub(wire other) {
        int maxwidth = Math.max(bitWidth, other.bitWidth);
        return new wire(maxwidth - 1, 0, value.subtract(other.value));
    }


    // *
    public wire mul(wire other) {
        return new wire(value.multiply(other.value));
    }

    // -
    public wire neg() {
        return new wire(bitWidth - 1, 0, value.negate());
    }

    //-------------------------- 移位操作 --------------------------
    
    // <<
    public wire shiftLeft(wire amount) {
        return new wire(value.shiftLeft(amount.value.intValue()));
    }
    public wire shiftLeft(BigInteger amount) {
        return new wire(value.shiftLeft(amount.intValue()));
    }
    public wire shiftLeft(int amount) {
        return new wire(value.shiftLeft(amount));
    }

    // >>
    public wire shiftRight(wire amount) {
        return new wire(bitWidth - 1, 0, value.shiftRight(amount.value.intValue()));
    }
    public wire shiftRight(BigInteger amount) {
        return new wire(bitWidth - 1, 0, value.shiftRight(amount.intValue()));
    }
    public wire shiftRight(int amount) {
        return new wire(bitWidth - 1, 0, value.shiftRight(amount));
    }

    //-------------------------- 关系运算 --------------------------
    // >
    public wire greaterThan(wire other) {
        boolean res = value.compareTo(other.value) > 0;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // <
    public wire lessThan(wire other) {
        boolean res = value.compareTo(other.value) < 0;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // >=
    public wire greaterEqual(wire other) {
        boolean res = value.compareTo(other.value) >= 0;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // <=
    public wire lessEqual(wire other) {
        boolean res = value.compareTo(other.value) <= 0;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // ==
    public wire isEqual(wire other) {
        boolean res = value.equals(other.value);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // !=
    public wire notEqual(wire other) {
        boolean res = !value.equals(other.value);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    //-------------------------- 归约操作 --------------------------
    
    // &
    public wire reduceAnd() {
        boolean res = value.bitCount() == bitWidth;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }
    // ^
    public wire reduceXor() {
        boolean res = value.bitCount() % 2 == 1;
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }
    // |
    public wire reduceOr() {
        boolean res = !value.equals(BigInteger.ZERO);
        return new wire(0, 0, res ? BigInteger.ONE : BigInteger.ZERO);
    }

    // 逻辑值
    public boolean notZero() {
        return !value.equals(BigInteger.ZERO);
    }
    //-------------------------- 三目运算 --------------------------

    // ? :
    public wire ternary(wire trueValue, wire falseValue) {
        int maxwidth = Math.max(trueValue.bitWidth, falseValue.bitWidth);
        return new wire(maxwidth - 1, 0, value.equals(BigInteger.ZERO) ? falseValue.value : trueValue.value);
    }


    //-------------------------- 其他接口 --------------------------

    public int getBitWidth() { return bitWidth; }
    public BigInteger get() { return value; }
    public wire clone() { return new wire(highBit, lowBit, value); }

    // 测试
    public static void main(String[] args) {
        wire a = new wire(3, 0, 0b1101); // 4-bit wire
        wire b = new wire(3, 0, 0b1010);

        // 按位与
        wire andResult = a.bitAnd(b);
        System.out.println(andResult.get().toString(2));    // 输出: 1000

        // 加法
        wire sum = a.add(b); // 0b1101 + 0b1010 = 0x17 (截断为4位: 0b0111)
        System.out.println(sum.get().toString(2));          // 输出: 111

        // 位拼接
        wire concated = wire.concat(a, new wire(1, 0, 0b00), b); // 10-bit: 0b1101001010
        System.out.println(concated.get().toString(2));     // 输出: 1101001010

        // 获取高位
        wire highBits = a.getBits(3, 2); // 获取第3、2位: 0b11
        System.out.println(highBits.get().toString(2));     // 输出: 11

        // 赋值
        a.set(b);
        System.out.println(a.get().toString(2));          // 输出: 1010

        // 局部赋值
        b.setBits(2, 1, 0b10);
        System.out.println(b.get().toString(2));          // 输出: 1100

        wire c = ZERO.ternary(new wire(22), new wire(11));
        System.out.println(c.get().toString(2));          // 输出: 1010

    }
}
