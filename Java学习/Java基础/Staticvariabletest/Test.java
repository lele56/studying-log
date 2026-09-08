package Staticvariabletest;

/**
 * 测试类：演示 static 静态变量的共享特性
 * 
 * 场景模拟：
 *   一个班级中，所有学生共享同一个老师
 *   - 第一名学生：小诗诗，19岁，老师是小文老师
 *   - 第二名学生：小丹丹，20岁，老师也是小文老师（共享）
 *   - 后来小丹丹申请换老师 → 小文老师换成小张老师
 *   - 小诗诗也自动换成了小张老师（因为 static 共享）
 * 
 * 关于 static 需要掌握的内容：
 *   1. 静态变量被当前类所有的对象共享
 *      - 赋值只需赋值一次，所有对象都能访问
 *      - 一个对象修改了静态变量，其他对象访问时就是修改后的结果
 *   2. 调用方式：
 *      - 方式一：类名调用（推荐）  → Student.teacher
 *      - 方式二：对象名调用（不推荐）→ stu1.teacher（会有警告）
 */
public class Test {
    public static void main(String[] args) {
        // ==================== 第一名学生：小诗诗 ====================
        Student stu1 = new Student();
        stu1.name = "小诗诗";       // 实例变量：只属于 stu1
        stu1.age = 19;             // 实例变量：只属于 stu1

        Student.teacher = "小文老师";  // 静态变量：用类名调用（推荐写法）
        // 此时所有 Student 对象共享的 teacher 都是 "小文老师"

        System.out.println(stu1.name + "的老师是：" + Student.teacher);

        // ==================== 第二名学生：小丹丹 ====================
        Student stu2 = new Student();
        stu2.name = "小丹丹";       // 实例变量：只属于 stu2
        stu2.age = 20;             // 实例变量：只属于 stu2

        // 没有重新设置 teacher，但 stu2 也能访问到同一个 teacher
        System.out.println(stu2.name + "的老师是：" + Student.teacher);

        System.out.println("------------------------");

        // ==================== 演示 static 共享特性 ====================
        System.out.println("小丹丹申请换老师...");
        Student.teacher = "小张老师";  // 通过类名修改静态变量

        // 所有对象看到的 teacher 都变了
        System.out.println(stu1.name + "的老师是：" + Student.teacher);
        System.out.println(stu2.name + "的老师是：" + Student.teacher);

        System.out.println("------------------------");

        // ==================== 验证：实例变量互不影响 ====================
        System.out.println("实例变量互不影响：");
        System.out.println("  stu1.name = " + stu1.name + ", stu1.age = " + stu1.age);
        System.out.println("  stu2.name = " + stu2.name + ", stu2.age = " + stu2.age);
        System.out.println("静态变量共享同一份：");
        System.out.println("  Student.teacher = " + Student.teacher);

        /*
         * 内存理解：
         * 
         *   堆内存（存对象）              方法区-静态区（存类信息）
         *   ┌─────────────┐             ┌──────────────────┐
         *   │ stu1 对象    │             │ Student 类       │
         *   │  name="小诗诗"│             │  teacher="小张老师"│ ← 只有一份
         *   │  age=19     │             └──────────────────┘
         *   └─────────────┘                ↑          ↑
         *   ┌─────────────┐                │          │
         *   │ stu2 对象    │                │          │
         *   │  name="小丹丹"│                │          │
         *   │  age=20     │                │          │
         *   └─────────────┘                │          │
         *        ↑                         │          │
         *        └──── 各自独立 ────────────┘──── 共享 ─┘
         */
    }
}