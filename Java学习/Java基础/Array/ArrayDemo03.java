package Array;

import java.util.Scanner;

public class ArrayDemo03 {
    public static void main(String[] args) {
        /*
        数组的动态初始化：
            需求：键盘录入 5 个整数，存入数组当中，并进行遍历

        动态初始化的格式：
            数据类型[] 数组名 = new 数据类型[数组长度];
         */

        // 创建数组
        int[] arr = new int[5];

        // 键盘录入数据
        Scanner sc = new Scanner(System.in);
        for (int i = 0; i < arr.length; i++) {
            System.out.println("请输入第" + (i + 1) + "个整数");
            arr[i] = sc.nextInt();
        }
        // 遍历数组
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
        sc.close();
    }
}
