package Method;

import java.util.Scanner;

public class Test03 {
    public static void main(String[] args) {
        /*
        计算快递邮费
        某快递公司的运费规则如下（首重 1 kg，超出部分按 kg 计算，不足 1 kg 时，按 1 kg 计算）：
        首重 1 kg：10 元；
        超出 1~5 kg：每 kg 加 2 元；
        超出 5 kg：每 kg 加 1.5 元；
        键盘录入小数，表示用户快递的重量，计算最终的结果
        要求1：快递重量必须大于 0，否则重新输入
        要求2：不同价位的计算，单独定义一个方法
        */
        Scanner sc = new Scanner(System.in);
        double weight;
        
        while (true) {
            System.out.println("请输入快递的重量（kg）：");
            
            if (!sc.hasNextDouble()) {
                System.out.println("请输入有效的数字！");
                sc.next();
                continue;
            }
            
            weight = sc.nextDouble();
            
            if (weight > 0) {
                break;
            }
            
            System.out.println("快递重量必须大于 0，请重新输入！");
        }
        
        double fee = getFee(weight);
        System.out.println("快递的邮费为：" + String.format("%.2f", fee));
        sc.close();
    }
    
    // 计算快递费
    public static double getFee(double weight) {
        // 不足 1kg 按 1kg 计算
        weight = Math.ceil(weight);
        
        if (weight <= 1) {
            return 10;
        }
        
        if (weight <= 5) {
            return 10 + (weight - 1) * 2;
        }
        
        // 首重 10 元 + 1~5kg 的 8 元 + 超出 5kg 部分
        return 10 + 8 + (weight - 5) * 1.5;
    }
}