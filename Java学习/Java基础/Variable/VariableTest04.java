package Variable;

import java.util.Scanner;

public class VariableTest04 {
    public static void main(String[] args) {
        /* 
         * BMI 身体质量指数计算公式：BMI = 体重 / 身高^2 （体重单位：千克，身高单位：米） 
         * 
         * BMI 数值（单位：千克/米^2）  | 健康风险 
         * 18.5 以下：消瘦              | 部分增加   
         * 18.5 - 23.9：正常            | 正常   
         * 24.0 - 26.9：偏胖            | 增加   
         * 27.0 - 29.9：肥胖            | 中度增加   
         * 30.0 以上：严重肥胖           | 严重增加   
         */

        // 从键盘输入体重和身高
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入体重（千克）：");
        double weight = sc.nextDouble();

        System.out.println("请输入身高（米）：");
        double height = sc.nextDouble();

        BMI bmi = new BMI(weight, height);

        System.out.println("---------------- 结果 ----------------");
        System.out.println("您的 BMI 值为：" + String.format("%.2f", bmi.value));
        System.out.println("您的身体状态为：" + bmi.getStatus());
        System.out.println("您的健康风险为：" + bmi.getRisk());
        
        sc.close();
    }
}

class BMI {
    double weight;
    double height;
    double value;  // 存放计算出的 BMI 值

    // BMI 计算公式：BMI = 体重 / 身高^2 （体重单位：千克，身高单位：米）
    public BMI(double weight, double height) {
        this.weight = weight;
        this.height = height;
        this.value = weight / (height * height);
    }

    // 获取身体状态
    public String getStatus() {
        if (value < 18.5) {
            return "消瘦";
        } else if (value < 24.0) {
            return "正常";
        } else if (value < 27.0) {
            return "偏胖";
        } else if (value < 30.0) {
            return "肥胖";
        } else {
            return "严重肥胖";
        }
    }

    // 获取健康风险
    public String getRisk() {
        if (value < 18.5) {
            return "部分增加";
        } else if (value < 24.0) {
            return "正常";
        } else if (value < 27.0) {
            return "增加";
        } else if (value < 30.0) {
            return "中度增加";
        } else {
            return "严重增加";
        }
    }
}
/*
【输出示例】
请输入体重（千克）：
50
请输入身高（米）：
1.78
---------------- 结果 ----------------
您的 BMI 值为：15.78
您的身体状态为：消瘦
您的健康风险为：部分增加
*/