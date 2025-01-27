"""
 * Initial code for Assignment 1, 2
 * Programming Language Principles
 * Author: Võ Tiến
 * Link FB : https://www.facebook.com/Shiba.Vo.Tien
 * Link Group : https://www.facebook.com/groups/khmt.ktmt.cse.bku
 * Date: 07.01.2025
"""

import unittest
from TestUtils import TestParser
import inspect

class ParserSuite(unittest.TestCase):
    def test_001(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = 1;","successful", inspect.stack()[0].function))

    def test_002(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = true;","successful", inspect.stack()[0].function))

    def test_003(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = [5][0]string{1, \"string\"};","successful", inspect.stack()[0].function))

    def test_004(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = [1.]ID{1, 3};","Error on line 1 col 16: 1.", inspect.stack()[0].function))

    def test_005(self):
        """Literal"""
        self.assertTrue(TestParser.test("const Votien = Person{name: \"Alice\", age: 30};","successful", inspect.stack()[0].function))

    def test_006(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = 1 || 2 && c + 3 / 2 - -1;","successful", inspect.stack()[0].function))

    def test_007(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = 1[2] + foo()[2] + ID[2].b.b;","successful", inspect.stack()[0].function))

    def test_008(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = ca.foo(132) + b.c[2];","successful", inspect.stack()[0].function))

    def test_009(self):
        """expression"""
        self.assertTrue(TestParser.test("const Votien = a.a.foo();","successful", inspect.stack()[0].function))

    def test_010(self):
        """declared variables"""
        self.assertTrue(TestParser.test("""
            var x int = foo() + 3 / 4;
            var y = "Hello" / 4;   
            var z str;
        ""","successful", inspect.stack()[0].function))

    def test_011(self):
        """declared constants"""
        self.assertTrue(TestParser.test("""
            const VoTien = a.b() + 2;
        ""","successful", inspect.stack()[0].function))

    def test_012(self):
        """declared function"""
        self.assertTrue(TestParser.test("""
            func VoTien(x int, y int) int {}
            func VoTien1() [2][3] ID {}         
            func VoTien2() {}                                       
        ""","successful", inspect.stack()[0].function))

    def test_013(self):
        """declared method"""
        self.assertTrue(TestParser.test("""
            func (c Calculator) VoTien(x int) int {}  
            func (c Calculator) VoTien() ID {}      
            func (c Calculator) VoTien(x int, y [2]VoTien) {}                                                      
        ""","successful", inspect.stack()[0].function))

    def test_014(self):
        """declared struct"""
        self.assertTrue(TestParser.test("""
            type VoTien struct {
                VoTien string ;
                VoTien [1][3]VoTien ;                     
            }
            type VoTien struct {}                                                                       
        ""","successful", inspect.stack()[0].function))

    def test_015(self):
        """declared Interface"""
        self.assertTrue(TestParser.test("""
            type VoTien struct {
                VoTien string ;
                VoTien [1][3]VoTien ;                     
            }
            type VoTien struct {}                                                                       
        ""","successful", inspect.stack()[0].function))

    def test_016(self):
        """declared Interface"""
        self.assertTrue(TestParser.test("""
            type Calculator interface {
                                        
                Add(x, y int) int;
                Subtract(a, b float, c int) [3]ID;
                Reset()
                                        
                SayHello(name string);
                                        
            }
            type VoTien interface {}                                                                       
        ""","successful", inspect.stack()[0].function))

    def test_017(self):
        """declared_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                var x int = foo() + 3 / 4;
                var y = "Hello" / 4;   
                var z str;
                                        
                const VoTien = a.b() + 2;
            }                                       
        ""","successful", inspect.stack()[0].function))


    def test_018(self):
        """assign_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                x  := foo() + 3 / 4;
                x.c[2][4] := 1 + 2;                       
            }                                       
        ""","successful", inspect.stack()[0].function))

    def test_019(self):
        """for_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                if (x > 10) {} 
                if (x > 10) {
                  
                } else if (x == 10) {
                    var z str;
                } else {
                    var z ID;
                }
            }
        ""","successful", inspect.stack()[0].function))

    def test_020(self):
        """if_statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {
                for i < 10 {}
                for i := 0; i < 10; i += 1 {}
                for index, value := range array {}
            }
        ""","successful", inspect.stack()[0].function))


    def test_021(self):
        """break and continue, return, Call  statement"""
        self.assertTrue(TestParser.test("""    
            func VoTien() {                           
                for i < 10 {break;}
                break;
                continue;
                return 1;
                return
                foo(2 + x, 4 / y); m.goo();                        
             }
                                        
        ""","successful", inspect.stack()[0].function))

    def test_022(self):
        """invalid_array_declaration"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = [2]int{};                           
        ""","Error on line 2 col 34: }", inspect.stack()[0].function))

    def test_031(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID {};                         
        ""","successful", inspect.stack()[0].function))

    def test_032(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = ID {a: 2, b: 2 + 2 + ID {a: 1}};                         
        ""","successful", inspect.stack()[0].function))

    def test_037(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a >= 2 <= "string" > a[2][3] < ID{A: 2} >= [2]S{2};                         
        ""","successful", inspect.stack()[0].function))


    def test_041(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            var z VOTIEN = a[2][3][a + 2];                         
        ""","successful", inspect.stack()[0].function))


    def test_042(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""
            var z VOTIEN = a[2, 3];                         
        ""","Error on line 2 col 30: ,", inspect.stack()[0].function))

    def test_052(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = ID {a : 2}.c[2] + 2[2] + true.foo() + (2).foo();                         
        ""","successful", inspect.stack()[0].function))

    def test_053(self):
        """Expressions"""
        self.assertTrue(TestParser.test("""    
            const k = -a + -!-!c - ---[2]int{2};                         
        ""","successful", inspect.stack()[0].function))

    def test_064(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            var c [2][3]ID
        ""","Error on line 2 col 26: \n", inspect.stack()[0].function))

    def test_086(self):
        """Declared"""
        self.assertTrue(TestParser.test("""    
            type Calculator interface {}
            type Person struct{};
""","successful", inspect.stack()[0].function))

    def test_105(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        const a = a[2].b
                                        var a = a[2].b; var a = "s";           
                                    }""","successful", inspect.stack()[0].function))
        
    def test_108(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a[2].b := 2;       
                                    }""","successful", inspect.stack()[0].function))
        
    def test_110(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.foo() += 2;       
                                    }""","Error on line 3 col 48: +=", inspect.stack()[0].function))
        
    def test_111(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        2 + 2 += 2;       
                                    }""","Error on line 3 col 40: 2", inspect.stack()[0].function))
        
    def test_109(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a.c[2].e[3].k += 2;       
                                    }""","successful", inspect.stack()[0].function))
        
    def test_113(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                       a[2+3&&2] += foo().b[2];       
                                    }""","successful", inspect.stack()[0].function))
        
    def test_118(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        if (x.foo().b[2]) 
                                        {
                                        } else if(1)
                                        {
                                        }else if(1)
                                        {
                                        }else if(2)
                                        {
                                        }else 
                                        {
                                        }
                                    }""","successful", inspect.stack()[0].function))
        
    def test_124(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for var i = 0; i < 10; i += 1 {
                                            // loop body
                                        }
                                    }""","successful", inspect.stack()[0].function))
        
    def test_125(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for const i = 0; i < 10; i += 1 {
                                            // loop body
                                        }
                                    }""","Error on line 3 col 44: const", inspect.stack()[0].function))
        
    def test_129(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        for index, value := range arr {
                                        // index: 0, 1, 2
                                        // value: 10, 20, 30
                                        }
                                    }""","successful", inspect.stack()[0].function))
        
    def test_143(self):
        """Statement"""
        self.assertTrue(TestParser.test("""
                                    func Add() {
                                        a[2][3].foo(2 + 3, a {a:2})
                                    }""","successful", inspect.stack()[0].function))
        