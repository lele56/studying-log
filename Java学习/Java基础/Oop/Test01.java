package Oop;

/**
 * 测试类：演示 Cook 类的使用
 * 
 * 演示内容：
 * 1. 使用有参构造创建对象
 * 2. 使用 getter/setter 访问属性（不能直接访问 private 属性）
 * 3. 方法重载的调用
 * 4. showInfo() 和 toString() 的使用
 */
public class Test01 {
    public static void main(String[] args) {
        // ==================== 方式一：有参构造创建对象 ====================
        System.out.println("==================== 方式一：有参构造 ====================");
        Cook cook1 = new Cook("张三", 30, 3);   // 创建时直接初始化

        cook1.showInfo();                       // 展示个人信息
        int exp1 = cook1.cooking();             // 无参烹饪：根据等级自动选择菜品
        System.out.println("  获得经验值：" + exp1 + "\n");

        // ==================== 方式二：无参构造 + setter 赋值 ====================
        System.out.println("==================== 方式二：无参构造 + setter ====================");
        Cook cook2 = new Cook();                // 先创建空对象
        cook2.setName("李四");                   // 再通过 setter 逐个赋值
        cook2.setAge(25);
        cook2.setCookLevel(5);                  // 设置等级为 5（厨神级别）

        cook2.showInfo();
        int exp2 = cook2.cooking();             // 等级 5，做满汉全席
        System.out.println("  获得经验值：" + exp2 + "\n");

        // ==================== 演示方法重载 ====================
        System.out.println("==================== 方法重载演示 ====================");

        Cook cook3 = new Cook("王五", 28, 4);

        // 重载1：无参，自动选菜
        cook3.cooking();

        // 重载2：指定菜名
        cook3.cooking("麻婆豆腐");

        // 重载3：指定菜名 + 火候
        cook3.cooking("清蒸鲈鱼", 2);  // 火候：2 = 中火

        System.out.println();

        // ==================== 演示 getter 方法 ====================
        System.out.println("==================== getter 方法演示 ====================");
        System.out.println("cook1 姓名：" + cook1.getName());
        System.out.println("cook1 年龄：" + cook1.getAge());
        System.out.println("cook1 等级：" + cook1.getCookLevel());

        System.out.println();

        // ==================== 演示 toString() ====================
        System.out.println("==================== toString() 演示 ====================");
        // 直接打印对象，会自动调用 toString() 方法
        System.out.println(cook1);
        System.out.println(cook2);
        System.out.println(cook3);

        System.out.println();

        // ==================== 演示数据校验 ====================
        System.out.println("==================== 数据校验演示 ====================");
        System.out.println("尝试设置非法年龄：");
        cook1.setAge(10);        // 不合法，会被拦截
        System.out.println("cook1 年龄仍为：" + cook1.getAge());

        System.out.println("尝试设置非法等级：");
        cook1.setCookLevel(100); // 不合法，会被拦截
        System.out.println("cook1 等级仍为：" + cook1.getCookLevel());
    }
}