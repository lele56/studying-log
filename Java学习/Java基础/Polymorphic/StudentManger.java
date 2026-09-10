package Polymorphic;

/**
 * 学生管理系统
 * 
 * 核心知识点：多态参数
 * register(Person person) 的参数类型是 Person，
 * 但实际可以传入 Student、Teacher、Admin 等任意子类对象
 * 
 * 这就是多态的最大优势：
 * 一个方法，可以处理所有子类型，不需要为每种角色写重载方法！
 */
public class StudentManger {

    /**
     * 注册用户
     * 
     * 多态参数：Person person 可以接收任意 Person 子类对象
     * - new Student(...)  → 注册学生
     * - new Teacher(...)  → 注册教师
     * - new Admin(...)    → 注册管理员
     * 
     * 不需要写三个重载方法：
     * register(Student s)、register(Teacher t)、register(Admin a)
     * 
     * @param person 要注册的用户（可以是任意子类）
     */
    public void register(Person person) {
        System.out.println("姓名为 " + person.getName()
                + " 的" + person.getRole() + "注册成功！"
                + "账号：" + person.getUsername()
                + "，密码：" + person.getPassword());
    }

    /**
     * 用户登录
     * 
     * @param person   登录用户
     * @param username 输入的账号
     * @param password 输入的密码
     * @return true 登录成功，false 登录失败
     */
    public boolean login(Person person, String username, String password) {
        if (person.getUsername().equals(username)
                && person.getPassword().equals(password)) {
            System.out.println(person.getRole() + " " + person.getName() + " 登录成功！");
            return true;
        } else {
            System.out.println("账号或密码错误，登录失败！");
            return false;
        }
    }
}