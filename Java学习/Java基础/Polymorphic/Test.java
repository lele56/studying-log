package Polymorphic;

/**
 * 测试类：演示多态
 * 
 * 继承体系：
 *        Person（父类）
 *        /   |   \
 *   Student Teacher Admin（子类）
 * 
 * 多态的核心演示：
 * 1. 方法参数多态：register(Person p) 接收所有子类
 * 2. 方法重写多态：p.work() 执行各自重写后的版本
 * 3. 多态数组：Person[] 统一管理所有角色
 */
public class Test {
    public static void main(String[] args) {

        // ==================== 1. 创建不同角色 ====================
        System.out.println("==================== 1. 创建不同角色 ====================");
        Student stu = new Student("张三", "zhangsan", "123456");
        Teacher tea = new Teacher("李老师", "lilaoshi", "654321");
        Admin admin = new Admin("王管理", "wangadmin", "111111");

        // ==================== 2. 多态参数：一个 register 方法注册所有角色 ====================
        System.out.println("\n==================== 2. 多态参数：统一注册 ====================");
        StudentManger sm = new StudentManger();

        // register(Person person) 可以接收任意子类对象
        sm.register(stu);   // 注册学生
        sm.register(tea);   // 注册教师
        sm.register(admin); // 注册管理员

        // 也可以直接在参数中 new 子类对象
        System.out.println("\n--- 直接 new 子类对象注册 ---");
        sm.register(new Student("赵六", "zhaoliu", "222222"));

        // ==================== 3. 多态方法：work() 各自不同实现 ====================
        System.out.println("\n==================== 3. 多态方法：work() 各自不同实现 ====================");
        stu.work();
        tea.work();
        admin.work();

        // ==================== 4. 多态数组：统一管理 ====================
        System.out.println("\n==================== 4. 多态数组：统一管理所有角色 ====================");
        Person[] users = { stu, tea, admin };

        System.out.println("--- 统一调用 work() ---");
        for (Person p : users) {
            p.work();  // 多态：实际执行哪个 work()，看对象类型
        }

        System.out.println("\n--- 统一调用 getRole() ---");
        for (Person p : users) {
            System.out.println(p.getName() + " 的角色是：" + p.getRole());
        }

        // ==================== 5. 登录演示 ====================
        System.out.println("\n==================== 5. 登录演示 ====================");
        sm.login(stu, "zhangsan", "123456");   // 正确登录
        sm.login(stu, "zhangsan", "wrong");    // 密码错误
        sm.login(tea, "lilaoshi", "654321");   // 教师登录

        // ==================== 6. 多态对比：不用多态 vs 用多态 ====================
        System.out.println("\n==================== 6. 多态 vs 不用多态 ====================");
        System.out.println("不用多态（需要写 3 个重载方法）：");
        System.out.println("  registerStudent(Student s) { ... }");
        System.out.println("  registerTeacher(Teacher t) { ... }");
        System.out.println("  registerAdmin(Admin a) { ... }");
        System.out.println("  如果新增角色，还要继续加方法！");
        System.out.println();
        System.out.println("用多态（只需 1 个方法）：");
        System.out.println("  register(Person p) { ... }");
        System.out.println("  新增角色只需继承 Person，无需修改 register！");
    }
}