package Oop;

/**
 * 厨师类
 * 封装了厨师的基本信息（姓名、年龄、厨艺等级）和行为（烹饪菜品）
 * 
 * 知识点：
 * 1. 封装：属性用 private 修饰，通过 getter/setter 访问
 * 2. 构造方法：创建对象时初始化属性
 * 3. this 关键字：区分成员变量和局部变量
 * 4. 方法重载：cooking 方法有多种不同参数形式
 */
public class Cook {
    // ==================== 属性（成员变量） ====================
    private String name;       // 厨师姓名
    private int age;           // 年龄
    private int cookLevel;     // 厨艺等级（1~5，数值越高越厉害）

    // ==================== 构造方法 ====================

    /**
     * 无参构造方法（默认构造）
     * 如果不写任何构造方法，Java 会自动生成一个无参构造
     */
    public Cook() {
    }

    /**
     * 有参构造方法：创建对象时直接初始化属性
     * @param name      厨师姓名
     * @param age       年龄
     * @param cookLevel 厨艺等级
     */
    public Cook(String name, int age, int cookLevel) {
        this.name = name;           // this.name 是成员变量，name 是参数
        this.age = age;
        this.cookLevel = cookLevel;
    }

    // ==================== Getter/Setter 方法 ====================
    // 封装原则：属性私有化，通过方法访问

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    /**
     * 设置年龄，增加合法性校验
     * @param age 年龄，必须在 18~65 之间
     */
    public void setAge(int age) {
        if (age >= 18 && age <= 65) {
            this.age = age;
        } else {
            System.out.println("年龄不合法，请输入 18~65 之间的值");
        }
    }

    public int getCookLevel() {
        return cookLevel;
    }

    /**
     * 设置厨艺等级，增加合法性校验
     * @param cookLevel 等级，必须在 1~5 之间
     */
    public void setCookLevel(int cookLevel) {
        if (cookLevel >= 1 && cookLevel <= 5) {
            this.cookLevel = cookLevel;
        } else {
            System.out.println("厨艺等级不合法，请输入 1~5 之间的值");
        }
    }

    // ==================== 行为方法 ====================

    /**
     * 烹饪菜品（无参版本）
     * 根据厨艺等级，烹饪不同水平的菜品
     * @return 烹饪所获得的经验值
     */
    public int cooking() {
        System.out.println(name + " 正在烹饪...");
        int exp = 0;  // 本次烹饪获得的经验值

        // 根据厨艺等级决定烹饪结果
        switch (cookLevel) {
            case 1:
                System.out.println("  做了一道番茄炒蛋，味道一般。");
                exp = 10;
                break;
            case 2:
                System.out.println("  做了一道宫保鸡丁，味道不错！");
                exp = 20;
                break;
            case 3:
                System.out.println("  做了一道红烧肉，色香味俱全！");
                exp = 30;
                break;
            case 4:
                System.out.println("  做了一道佛跳墙，香气四溢！");
                exp = 40;
                break;
            case 5:
                System.out.println("  做了一道满汉全席，厨神级别！");
                exp = 50;
                break;
        }
        return exp;
    }

    /**
     * 烹饪指定菜品（方法重载：参数不同）
     * @param dishName 菜品名称
     * @return 烹饪所获得的经验值
     */
    public int cooking(String dishName) {
        System.out.println(name + " 正在烹饪「" + dishName + "」...");
        // 等级越高，烹饪得分越高
        int exp = cookLevel * 15;
        System.out.println("  烹饪完成！获得经验值：" + exp);
        return exp;
    }

    /**
     * 烹饪指定菜品并控制火候（方法重载：两个参数）
     * @param dishName  菜品名称
     * @param fireLevel 火候（1=小火, 2=中火, 3=大火）
     * @return 烹饪所获得的经验值
     */
    public int cooking(String dishName, int fireLevel) {
        String fireStr;
        switch (fireLevel) {
            case 1: fireStr = "小火"; break;
            case 2: fireStr = "中火"; break;
            case 3: fireStr = "大火"; break;
            default: fireStr = "默认火候";
        }
        System.out.println(name + " 正在用「" + fireStr + "」烹饪「" + dishName + "」...");
        int exp = cookLevel * 10 + fireLevel * 5;
        System.out.println("  烹饪完成！获得经验值：" + exp);
        return exp;
    }

    /**
     * 展示厨师的个人信息
     */
    public void showInfo() {
        System.out.println("==================== 厨师信息 ====================");
        System.out.println("  姓名：" + name);
        System.out.println("  年龄：" + age + " 岁");
        System.out.println("  厨艺等级：" + "★".repeat(cookLevel) + " (" + cookLevel + " 级)");
        System.out.println("==================================================");
    }

    /**
     * 重写 toString() 方法，方便打印对象信息
     * 当直接 System.out.println(cook对象) 时会自动调用此方法
     */
    @Override
    public String toString() {
        return "Cook{姓名='" + name + "', 年龄=" + age + ", 等级=" + cookLevel + "}";
    }
}