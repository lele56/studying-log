package LoopWhile;

public class WhileDome03 {
    public static void main(String[] args) {
        /*
        需求：世界最高山峰珠穆朗玛峰高度是：8848.86米 = 8848860毫米，
        假如我有一张足够大的纸，它的厚度是 0.1 毫米。
        请问：该纸张折叠多少次，可以折成珠穆朗玛峰的高度？
        */
        int fold = 0;
        double thickness = 0.1;
        while (thickness < 8848860) {
            thickness *= 2;
            fold++;
        }
        System.out.println("需要 " + fold + " 次折叠才能折成珠穆朗玛峰的高度");
    }
}

// 输出结果
// 需要 27 次折叠才能折成珠穆朗玛峰的高度