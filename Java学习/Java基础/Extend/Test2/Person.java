package Extend.Test2;

/**
 * 人类（顶层父类）
 * 
 * 三层继承链：
 * Object → Person → Student → UndergradStudent/MasterStudent
 * Object → Person → Teacher → GeneralTeacher/MajorTeacher
 * 
 * 多层继承的特点：
 * 1. 子类可以继承"爷爷类"的属性和方法
 * 2. 每一层都可以添加自己的特有属性和方法
 * 3. 每一层都可以重写父类的方法
 */
public class Person {
    // ==================== 成员变量 ====================
    private String name;  // 姓名
    private int age;      // 年龄

    // ==================== 构造方法 ====================
    public Person() {
    }

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    // ==================== Getter/Setter ====================
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    // ==================== 行为方法 ====================
    /**
     * 吃饭方法
     * 子类可以重写此方法
     */
    public void eat() {
        System.out.println(name + " 正在吃饭");
    }

    /**
     * 睡觉方法
     */
    public void sleep() {
        System.out.println(name + " 正在睡觉");
    }

    /**
     * 展示个人信息
     * 子类可以重写以展示更多信息
     */
    public void showInfo() {
        System.out.println("姓名：" + name + "，年龄：" + age + " 岁");
    }
}