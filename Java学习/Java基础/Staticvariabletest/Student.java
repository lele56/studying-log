package Staticvariabletest;

/**
 * 学生类
 * 演示 static 静态变量的用法
 * 
 * static 关键字说明：
 * 1. static 修饰的变量属于「类本身」，不属于某个对象
 * 2. 所有对象共享同一份 static 变量，存在方法区的静态区中
 * 3. 一个对象修改了 static 变量，其他对象访问时也会看到修改后的值
 */
public class Student {
    String name;           // 实例变量：每个对象都有自己的一份
    int age;               // 实例变量：每个对象都有自己的一份
    static String teacher; // 静态变量：所有对象共享同一份
}