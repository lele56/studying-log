package Extend.Test1;

/**
 * 人类（父类/基类）
 * 
 * 继承知识点：
 * 
 * 1. 什么是继承？
 *    子类（Student/Teacher）通过 extends 关键字继承父类（Person）的属性和方法
 *    相当于子类"拥有"了父类的所有非私有成员
 * 
 * 2. 继承的好处：
 *    - 代码复用：子类不需要重复写 name、age 和 eat() 方法
 *    - 多态的基础：父类引用可以指向子类对象
 * 
 * 3. Java 继承的特点：
 *    - 单继承：一个类只能有一个直接父类（但可以多层继承）
 *    - 所有类默认继承 Object 类
 *    - 子类不能继承父类的构造方法，但可以通过 super() 调用
 * 
 * 4. 访问权限对继承的影响：
 *    - private   ：子类不能直接访问，但可以通过 getter/setter 访问
 *    - 默认      ：同包子类可以访问
 *    - protected ：不同包子类也可以访问
 *    - public    ：所有类都可以访问
 */
public class Person {
    // ==================== 成员变量 ====================
    private String name;  // 姓名
    private int age;      // 年龄

    // ==================== 构造方法 ====================
    /**
     * 无参构造
     * 当子类调用 super() 时，会调用父类的无参构造
     */
    public Person() {
    }

    /**
     * 有参构造
     * @param name 姓名
     * @param age  年龄
     */
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
     * 子类可以继承此方法，也可以重写（Override）
     */
    public void eat() {
        System.out.println(name + " 在吃饭");
    }

    /**
     * 睡觉方法
     * 所有人类都有的行为，子类直接继承即可
     */
    public void sleep() {
        System.out.println(name + " 在睡觉");
    }

    /**
     * 展示个人信息
     * 子类可以重写此方法来展示更多信息
     */
    public void showInfo() {
        System.out.println("姓名：" + name + "，年龄：" + age + " 岁");
    }

    /**
     * 重写 Object 类的 toString 方法
     */
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
}