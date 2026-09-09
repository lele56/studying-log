package Extend.Test1;

/**
 * 测试类：演示继承的各种用法
 * 
 * 继承的三大核心知识点：
 * 1. 继承（extends）：子类拥有父类的属性和方法
 * 2. 重写（Override）：子类重新定义父类的方法
 * 3. 多态（Polymorphism）：父类引用指向子类对象
 */
public class Test {
    public static void main(String[] args) {

        // ==================== 1. 基本使用：子类继承父类方法 ====================
        System.out.println("==================== 1. 子类继承父类方法 ====================");
        Student stu = new Student("张三", 20, "大二");
        // 子类可以直接调用父类的方法
        stu.sleep();   // 继承自 Person
        stu.study();   // Student 特有的方法

        Teacher tea = new Teacher("李老师", 35, "数学");
        tea.sleep();   // 继承自 Person
        tea.teach();   // Teacher 特有的方法

        // ==================== 2. 方法重写 ====================
        System.out.println("\n==================== 2. 方法重写（Override） ====================");
        // 子类重写了 eat() 方法，调用的是子类自己的版本
        stu.eat();     // 调用 Student 重写后的 eat()
        tea.eat();     // 调用 Teacher 重写后的 eat()

        // ==================== 3. 多态：父类引用指向子类对象 ====================
        System.out.println("\n==================== 3. 多态 ====================");
        // 父类类型 变量名 = new 子类类型()
        Person p1 = new Student("王五", 21, "大三");
        Person p2 = new Teacher("赵老师", 40, "英语");

        // 多态调用：编译看左边，运行看右边
        // 编译时：p1 是 Person 类型，能调用 Person 的方法
        // 运行时：p1 实际是 Student 对象，执行 Student 重写后的方法
        p1.eat();   // 运行的是 Student 的 eat()
        p2.eat();   // 运行的是 Teacher 的 eat()

        p1.showInfo();
        System.out.println("---");
        p2.showInfo();

        // ==================== 4. 多态的应用：统一处理不同类型 ====================
        System.out.println("\n==================== 4. 多态的应用 ====================");
        // 可以用父类数组存放不同类型的子类对象
        Person[] people = {
            new Student("小明", 18, "大一"),
            new Student("小红", 19, "大二"),
            new Teacher("张老师", 45, "物理"),
            new Teacher("王老师", 38, "化学")
        };

        // 统一遍历，调用 eat() 方法
        // 不用关心每个对象具体是 Student 还是 Teacher，统一按 Person 处理
        for (Person p : people) {
            p.eat();  // 多态：实际执行各自重写后的方法
        }

        // ==================== 5. super 关键字：调用父类方法 ====================
        System.out.println("\n==================== 5. super 关键字 ====================");
        // showInfo() 中先用 super.showInfo() 调用父类方法，再输出子类信息
        stu.showInfo();
        System.out.println("---");
        tea.showInfo();

        // ==================== 6. instanceof 判断类型 ====================
        System.out.println("\n==================== 6. instanceof 判断类型 ====================");
        for (Person p : people) {
            if (p instanceof Student) {
                // 向下转型：Person → Student
                Student s = (Student) p;
                System.out.println(s.getName() + " 是学生，年级：" + s.getGrade());
            } else if (p instanceof Teacher) {
                // 向下转型：Person → Teacher
                Teacher t = (Teacher) p;
                System.out.println(t.getName() + " 是老师，科目：" + t.getSubject());
            }
        }
    }
}