> Go 使用 struct 来实现类似面向对象语言中的 class，那么继承&多继承自然也是围绕 struct 来实现的

现在有 Person 和 Student 两个 struct：
```go
type Person struct {
  Name string
}

func (self Person) Say() {
  fmt.Println("I'm " + self.Name)
}

type Student struct {
  School string
}

func (self Student) Study() {
  fmt.Println("Studying...")
}
```

如何能够让 Student 继承 Person 的属性和方法呢？

主要有两种方法：组合、内嵌

## 组合

组合就是将“父类”作为“子类”的一个具名字段，在需要调用“父类”属性/方法的时候需要通过该字段去调用。

```go
type Student struct {
  School string
  person *Person
}

func (self Student) Person() *Person {
  return self.person
}
```
```go
func main() {
  p := &Person{"Nick"}
  stu := &Student{School: "SCUT", person: p}
  fmt.Println(stu.Person().Say())
}
```

## 内嵌
内嵌则是更类似于面向对象语言中的继承，是将结构体作为匿名字段
```go
type Student struct {
  Person
  School string
}

func main() {
  s := &Student{Person{"Nick"}, "SCUT"}
  s.Say()
}
```

## 多继承
以上两种方式都可以实现类似多继承的效果，也就是多几个字段而已。

需要额外注意的是：
1. 如果同一层有两个或以上同名字段，且子层没有该字段的实现时，会编译错误。

	如
    ```go
	type A struct {
      a, b string
    }

	type B struct {
      b, c int
    }

	type C struct {
      A
      B
    }

	c := C{}
	fmt.Println(c.a)  // 未调用 b 属性时不会报错
	fmt.Println(c.b)  // 编译错误
	```
    
    但是如果在 C 里重载 b 属性：
    ```go
	type C struct {
      A
      B
      b bool
    }
    ```
    此时可以正常运行。

2. 无法通过多继承来实现多态
	先举一个典型的栗子：python 中的 mixin
    ```python
	class ErrorMixin:
    	# 真正的 mixin 一般是不需要实现这个方法的了，
        # 这里为了和静态语言比较还是写明了
    	def __str__(self):
        	return 'base'
    
    	def error_message(self):
        	return self.__str__()
	
	class A(ErrorMixin):
    	def __str__(self):
        	return 'a'
	
	class B(ErrorMixin):
    	def __str__(self):
        	return 'b'

	a = A()
	b = B()
	print(a.error_message())	# 'a'
	print(b.error_message())	# 'b'
    ```
    
    再来看看 go 会是怎样：
    ```go
	type A struct{}

	type B struct{
      A
    }
	
	func (A) String() {
      fmt.Println("a")
    }

	func (self A) ErrorMsg() {
      self.String()
    }

	func (B) String() {
      fmt.Println("b")
    }

	b := &B{A{}}
	b.String()
	b.ErrorMsg()
	```
    执行后会发现，b.String() 打印出预料中的 "b"，但是 b.ErrorMsg() 却打印出了 "a"。
    
    这是因为 B 虽然通过内嵌获得了 A 的属性和方法，但是 ErrorMsg 方法本质上还是 A 的方法，内部调用的也是 A.String() 方法。
    
    这点使用继承的时候也需要额外注意。
    
    相比面向对象语言，go 提供了一种更强大、却更简单的多态行为——接口(interface)
    
    
    
    
    
    
    