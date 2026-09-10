package Polymorphic;

/**
 * 人类（父类）
 * 
 * 多态的核心：父类类型作为参数，可以接收任意子类对象
 * StudentManger.register(Person p) 可以接收 Student、Teacher、Admin
 * 
 * 多态的两种形式：
 * 1. 方法参数多态：register(Person p) → 传任意子类
 * 2. 方法重写多态：p.work() → 实际执行哪个，看 p 指向的对象类型
 */
public class Person {
    // ==================== 成员变量 ====================
    private String name;      // 姓名
    private String username;  // 账号
    private String password;  // 密码

    // ==================== 构造方法 ====================
    public Person() {
    }

    public Person(String name, String username, String password) {
        this.name = name;
        this.username = username;
        this.password = password;
    }

    // ==================== Getter/Setter ====================
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    // ==================== 行为方法 ====================
    /**
     * 工作方法
     * 每个子类重写此方法，实现各自的工作内容
     * 多态调用：p.work() 实际执行的是 p 指向对象的 work() 版本
     */
    public void work() {
        System.out.println("人在工作");
    }

    /**
     * 获取角色名称
     * 子类重写以返回具体角色名（如"学生"、"教师"）
     */
    public String getRole() {
        return "用户";
    }
}