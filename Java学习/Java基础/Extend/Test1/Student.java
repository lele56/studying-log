package Extend.Test1;

/**
 * 学生类（子类/派生类）
 * 继承 Person 类，拥有 Person 的所有属性和方法
 * 
 * 继承语法：
 * public class Student extends Person { }
 * 
 * 继承链：
 * Object → Person → Student
 * 
 * 子类能做什么：
 * 1. 直接使用父类的非私有成员（name, age, eat()）
 * 2. 添加自己的属性和方法（grade, study()）
 * 3. 重写父类的方法（Override）
 */
public class Student extends Person {
    // ==================== 特有属性 ====================
    private String grade;  // 年级，如：大一、大二

    // ==================== 构造方法 ====================
    /**
     * 无参构造
     * 默认调用父类的无参构造 super()
     */
    public Student() {
        super();  // 调用父类无参构造（可省略，Java 会自动添加）
    }

    /**
     * 有参构造
     * 通过 super(name, age) 调用父类的有参构造
     * 
     * @param name  姓名
     * @param age   年龄
     * @param grade 年级
     */
    public Student(String name, int age, String grade) {
        super(name, age);  // 必须放在第一行，调用父类的有参构造
        this.grade = grade;
    }

    // ==================== Getter/Setter ====================
    public String getGrade() {
        return grade;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    // ==================== 特有方法 ====================
    /**
     * 学生学习的方法（子类特有的方法）
     */
    public void study() {
        // getName() 是父类的方法，子类可以直接调用
        System.out.println(getName() + " 正在学习...");
    }

    // ==================== 重写父类方法 ====================
    /**
     * 重写（Override）父类的 showInfo 方法
     * 加上子类特有的年级信息
     * 
     * @Override 注解的作用：
     * 1. 告诉编译器这是重写方法，帮你检查方法签名是否正确
     * 2. 提高代码可读性
     */
    @Override
    public void showInfo() {
        // 先调用父类的 showInfo 方法
        super.showInfo();
        // 再输出子类特有的信息
        System.out.println("年级：" + grade);
    }

    /**
     * 重写父类的 eat 方法
     * 学生吃饭比较快！
     */
    @Override
    public void eat() {
        System.out.println(getName() + " 飞快地吃完饭，赶去上课！");
    }
}