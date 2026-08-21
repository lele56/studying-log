// package Java学习.Java基础;
// package：表示当前的类定义在哪个包下。
// 这里，将包路径写到 .vscode 的 settings.json 中，设置"java.project.sourcePaths": ["Java学习/Java基础"]，就可以不写包路径了。

// 定义一个类
// class：表示定义一个类
// 类名：HelloWorld
// {}：表示类的范围，所有代码都需要写在这个大括号当中
public class HelloWorld {
    // 表示 java 程序的主入口，当程序开始运行的时候，会从主入口开始逐行往下运行
    // 固定格式
    public static void main(String[] args) {
/*      细节一：
                修改注释的颜色
        细节二： 
                注释的快捷键
                vscode 多行是 shift + alt + a 
        细节三：
                注释的运行规则
                注释不会影响程序的运行
        细节四：
                注释的嵌套
        */
       // 输出 Hello, World!
        System.out.println("Hello, World!");
    }
}