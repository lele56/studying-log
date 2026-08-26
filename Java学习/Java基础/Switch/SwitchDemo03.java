package Switch;

public class SwitchDemo03 {
    public static void main(String[] args) {
        /*
        switch 新特性
        1. 箭头标签
        2. case 后面可以写多个值
        3. switch 可以有运行结果
        4. yield 关键字
        */

        int num = 3;

        // yield 关键字：用于返回 switch 表达式的的结果，而不是 break 或 continue
        // 一行代码情况下，yield 也可以省略，直接返回表达式的值
        String result = switch (num) {
            case 1, 2 -> {
                yield "1";
            }
            case 3 -> {
                yield "3";
            }
            default -> "其他";
        };
        System.out.println(result);
    }
}
