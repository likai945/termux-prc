//Nov 2, 2024
//by LiKai

package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"os"
	//	"path/filepath"
	"strconv"
	"strings"
	//	"time"
	"github.com/xuri/excelize/v2"
)

var f = excelize.NewFile()
var smrr, hisr, crtr int
var totalmap = map[string]string{}
var date string = "2024-11-03"

func readFile(fl string) [][]string {
	file, _ := os.Open(fl)
	defer file.Close()

	obj := csv.NewReader(file)

	var sli [][]string
	for {
		record, err := obj.Read()
		if err == io.EOF {
			break
		}
		sli = append(sli, record)
	}
	return sli[1:]
}

func toDisc(file string, indx int) map[string][3][]string {
	alrmsli := readFile(file)
	amap := map[string][3][]string{}
	for _, row := range alrmsli {
		desc := row[indx]
		rowval := amap[desc]
		sttt := append(rowval[0], row[7])
		endt := append(rowval[1], row[9])
		devi := append(rowval[2], row[5]+"名="+row[6])
		amap[desc] = [3][]string{sttt, endt, devi}
	}
	return amap
}

func toWall(file string, indx int) [][]string {
	amap := toDisc(file, indx)
	resmap := toDict()
	var sum int
	var lines [][]string
	for key, val := range amap {
		desc := key
		sttt := strings.Join(val[0], "\n")
		endt := strings.Join(val[1], "\n")
		devi := strings.Join(val[2], "\n")
		nu := len(val[2])
		sum += nu
		num := strconv.Itoa(nu)
		res := resmap[desc]
		var line []string
		if indx == 3 {
			line = []string{sttt, endt, devi, desc, num, res, "是"}
		} else if indx == 4 {
			line = []string{sttt, endt, devi, desc, num, res}
		}
		lines = append(lines, line)
	}
	totalmap[file] = strconv.Itoa(sum)
	return lines
}

//	func checkFile(file){
//		if if
//	}
func writeFrm(sheet string, line []string) {
	for fld, cell := range line {
		field := int(rune('A')) + fld
		cellcrd := string(field) + "1"
		f.SetCellValue(sheet, cellcrd, cell)
	}
}

func init() {
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()
	f.NewSheet("Sheet2")
	f.NewSheet("Sheet3")

	smrtitle := []string{"时间", "资源池", "历史告警数", "当前告警数量", "当前告警清除数量", "当前告警剩余"}
	histitle := []string{"时间", "资源池", "告警时间", "清除时间", "对象名称", "告警描述", "数量", "处理结果"}
	crttitle := []string{"时间", "资源池", "告警时间", "确认恢复时间", "对象名称", "告警描述", "数量", "处理结果", "是否清除", "未确认恢复原因"}

	writeFrm("Sheet1", smrtitle)
	writeFrm("Sheet2", histitle)
	writeFrm("Sheet3", crttitle)

	smrr++
	hisr++
	crtr++
}

func isNumberic(str string) bool {
	_, err := strconv.Atoi(str)
	return err == nil
}

func writeSheet(sheet, pool string, ruler int, lines [][]string) {
	//	datest:="A"+strconv.Itoa(ruler+1)
	poolst := "B" + strconv.Itoa(ruler+1)

	f.SetCellValue(sheet, "A2", date)
	f.SetCellValue(sheet, poolst, pool)

	for rownum, line := range lines {
		for fieldnum, cell := range line {
			field := int(rune('C')) + fieldnum
			row := strconv.Itoa(rownum + ruler + 1)
			cellcrd := string(field) + row
			datecrd := "A" + row
			poolcrd := "B" + row

			if isNumberic(cell) {
				numcell, _ := strconv.Atoi(cell)
				f.SetCellValue(sheet, cellcrd, numcell)
			} else {
				f.SetCellValue(sheet, cellcrd, cell)
			}

			f.MergeCell(sheet, "A2", datecrd)
			f.MergeCell(sheet, poolst, poolcrd)

			ruler, _ := strconv.Atoi(row)
			switch sheet {
			case "Sheet1":
				smrr = ruler
			case "Sheet2":
				hisr = ruler
			case "Sheet3":
				crtr = ruler
			}
		}
	}

}

func main() {
	//	pools:=readFile("config")[0]
	writeSheet("Sheet2", "可信3", hisr, toWall("h3.csv", 4))
	writeSheet("Sheet2", "可信4", hisr, toWall("h4.csv", 4))
	writeSheet("Sheet2", "可信5", hisr, toWall("h5.csv", 4))
	writeSheet("Sheet2", "DMZ9", hisr, toWall("h9.csv", 4))
	writeSheet("Sheet2", "可信11", hisr, toWall("h11.csv", 4))

	writeSheet("Sheet3", "可信3", crtr, toWall("c3.csv", 3))
	writeSheet("Sheet3", "可信4", crtr, toWall("c4.csv", 3))
	writeSheet("Sheet3", "可信5", crtr, toWall("c5.csv", 3))
	writeSheet("Sheet3", "DMZ9", crtr, toWall("c9.csv", 3))
	writeSheet("Sheet3", "可信11", crtr, toWall("c11.csv", 3))

	writeSheet("Sheet1", "可信3", smrr, getKey("3"))
	writeSheet("Sheet1", "可信4", smrr, getKey("4"))
	writeSheet("Sheet1", "可信5", smrr, getKey("5"))
	writeSheet("Sheet1", "DMZ9", smrr, getKey("9"))
	writeSheet("Sheet1", "可信11", smrr, getKey("11"))
	after()
	//    err = f.MergeCell("Sheet1", "B2", "C5")
	//    f.SetActiveSheet(index)
}

func toDict() map[string]string {
	resarr := readFile("result.csv")
	amap := map[string]string{}
	for _, val := range resarr {
		amap[val[0]] = val[1]
	}
	return amap
}

func after() {
	f.InsertRows("Sheet2", 1, 1)
	f.SetCellValue("Sheet2", "A1", "历史告警")
	f.MergeCell("Sheet2", "A1", "H1")
	f.InsertRows("Sheet3", 1, 1)
	f.SetCellValue("Sheet3", "A1", "当前告警")
	f.MergeCell("Sheet3", "A1", "J1")

	f.SetSheetName("Sheet1", "汇总")
	f.SetSheetName("Sheet2", "历史告警处理记录")
	f.SetSheetName("Sheet3", "当前告警处理记录")

	if err := f.SaveAs("Book1.xlsx"); err != nil {
		fmt.Println(err)
	}
}

func defaultKey(key, defkey string, anymap map[string]string) string {
	_, exist := anymap[key]
	if exist {
		return anymap[key]
	} else {
		return defkey
	}
}

func getKey(key string) [][]string {
	lines := [][]string{}
	hiscsv := fmt.Sprintf("h%s.csv", key)
	crtcsv := fmt.Sprintf("c%s.csv", key)
	totalhis := defaultKey(hiscsv, "0", totalmap)
	totalcrt := defaultKey(crtcsv, "0", totalmap)
	lines = append(lines, []string{totalhis, totalcrt, totalcrt, "0"})
	return lines
}
