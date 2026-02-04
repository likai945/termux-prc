// Dec 1, 2024 the very beginning
// Jul 30, 2025 update for removing rocks
// Jan 23, 2026 no need to unzip manually
// Jan 29, 2026 no need to rename files
// Feb 4, 2026 change the way to get indexies
// by LiKai

package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/dablelv/cyan/zip"
	"github.com/xuri/excelize/v2"
)

var (
	f                = excelize.NewFile()
	smrr, hisr, crtr int
	totalmap                = map[string]string{}
	currentTime             = getTime()
	date             string = currentTime.Format("2006-01-02")
	namedate         string = currentTime.Format("20060102")
	bookname         string = fmt.Sprintf("附件3：告警分析-中兴资源池-%s.xlsx", namedate)
	pools                   = []string{"可信3", "可信4", "可信5", "DMZ9", "可信11", "可信14", "DMZ16", "可信17"}
	timedict                = map[string]string{}
	timefill         string = "auto"
	styletype        string = "format"
	unget                   = []string{}
	tmpfiles                = []string{}
)

func main() {
	renameZiles()
	renameCiles()
	before()
	if fileExist("config") {
		pools = readFile("config")[1]
	}
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.csv", nums[0])
		hfile := fmt.Sprintf("h%s.csv", nums[0])
		writeSheet("Sheet2", pool, hisr, checkExist(hfile, pool))
		writeSheet("Sheet3", pool, crtr, checkExist(cfile, pool))
		writeSheet("Sheet1", pool, smrr, getKey(nums[0]))
	}
	after()
}

func getTime() time.Time {
	ctime := time.Now()
	cstSh, err := time.LoadLocation("Asia/Shanghai")
	if err == nil {
		ctime = ctime.In(cstSh)
	}
	return ctime
}

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
	return sli
}

func toDisc(file string) map[string][3][]string {
	allsli := readFile(file)
	title := allsli[0]
	desci := getIndex("告警描述", title)
	sttti := getIndex("发生时间", title)
	eti := getIndex("恢复时间", title)
	typei := getIndex("对象类型", title)
	devi := getIndex("对象名称", title)

	alrmsli := allsli[1:]
	amap := map[string][3][]string{}
	for _, row := range alrmsli {
		desc := row[desci]
		rowval := amap[desc]
		sttt := append(rowval[0], row[sttti])
		et := defaultKey(file, row[eti], timedict)
		endt := append(rowval[1], et)
		dev := append(rowval[2], row[typei]+"名="+row[devi])
		amap[desc] = [3][]string{sttt, endt, dev}
	}
	return amap
}

func getIndex(val string, arr []string) int {
	for i, v := range arr {
		if val == v {
			return i
		}
	}
	return 0
}

func toWall(file string) [][]string {
	amap := toDisc(file)
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
		if file[0:1] == "c" {
			line = []string{sttt, endt, devi, desc, num, res, "是"}
		} else if file[0:1] == "h" {
			line = []string{sttt, endt, devi, desc, num, res}
		}
		lines = append(lines, line)
	}
	totalmap[file] = strconv.Itoa(sum)
	return lines
}

func writeFrm(sheet string, line []string) {
	for fld, cell := range line {
		field := int(rune('A')) + fld
		cellcrd := string(field) + "1"
		f.SetCellValue(sheet, cellcrd, cell)
	}
}

func before() {
	defer func() {
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()
	f.NewSheet("Sheet2")
	f.NewSheet("Sheet3")

	smrtitle := []string{"时间", "资源池", "历史告警数量", "当前告警数量", "当前告警清除数量", "当前告警剩余"}
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

func checkExist(file, pool string) [][]string {
	hcmap := map[string][][]string{
		"h": {{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及"}},
		"c": {{"无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "无告警，不涉及", "0", "无告警，不涉及", "是"}},
	}
	hcchmap := map[string]string{"h": "历史", "c": "当前"}
	fexist, _ := filepath.Glob(file)
	var command string
	if fileExist("config") {
		timefill = readFile("config")[3][0]
	}
	if len(fexist) == 0 {
		fmt.Printf("\033[32m%s\033[0m不存在,若\033[32m%s\033[0m无\033[32m%s\033[0m告警，请输入OK，否则输入NG以退出。\n", file, pool, hcchmap[file[0:1]])
		fmt.Scanln(&command)
		if strings.EqualFold(command, "OK") {
			return hcmap[file[0:1]]
		} else {
			rmFiles()
			os.Exit(2)
		}
	}

	if file[0:1] == "c" && timefill == "auto" {
		timedict[file] = currentTime.Format("2006-01-02 03:04:05")
	} else if file[0:1] == "c" && timefill == "no" {
		fmt.Printf("%s当前告警清除时间：", pool)
		reader := bufio.NewReader(os.Stdin)
		pdeltime, _ := reader.ReadString('\n')
		deltime := strings.TrimRight(pdeltime, "\n")
		timedict[file] = deltime
	}
	return toWall(file)
}

func toDict() map[string]string {
	var resarr [][]string
	amap := map[string]string{}
	if fileExist("result.csv") {
		resarr = readFile("result.csv")
	} else {
		return amap
	}
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

	if fileExist("config") {
		styletype = readFile("config")[5][0]
	}
	if styletype == "format" {
		style()
	} else {
		styless()
	}

	f.SetSheetName("Sheet1", "汇总")
	f.SetSheetName("Sheet2", "历史告警处理记录")
	f.SetSheetName("Sheet3", "当前告警处理记录")

	f.SaveAs(bookname)
	mvFiles()
}

func style() {
	styleIdnc := filling("left")
	styleIdc := filling("center")

	sfar := fmt.Sprintf("F%d", smrr)
	hfar := fmt.Sprintf("H%d", hisr+1)
	cfar := fmt.Sprintf("J%d", crtr+1)
	chcolfar := fmt.Sprintf("H%d", crtr+1)
	hcent := fmt.Sprintf("B%d", hisr+1)
	ccent := fmt.Sprintf("B%d", crtr+1)
	hcl := fmt.Sprintf("G%d", hisr+1)
	ccl := fmt.Sprintf("I%d", crtr+1)
	f.SetCellStyle("Sheet1", "A1", sfar, styleIdc)

	f.SetCellStyle("Sheet2", "C1", hfar, styleIdnc)
	f.SetCellStyle("Sheet2", "A3", hcent, styleIdc)
	f.SetCellStyle("Sheet2", "G3", hcl, styleIdc)
	f.SetCellStyle("Sheet2", "A1", "H2", styleIdc)

	f.SetCellStyle("Sheet3", "C1", cfar, styleIdnc)
	f.SetCellStyle("Sheet3", "A3", ccent, styleIdc)
	f.SetCellStyle("Sheet3", "G3", ccl, styleIdc)
	f.SetCellStyle("Sheet3", "A1", "J2", styleIdc)
	f.SetCellStyle("Sheet3", "H1", chcolfar, styleIdnc)

	smwdth := map[string]float64{"A": 11, "B": 7, "C": 13, "D": 13, "E": 17, "F": 13}
	hcwdth := map[string]float64{"A": 11, "B": 8, "C": 20, "D": 20, "E": 45, "F": 22, "G": 6, "H": 26, "I": 10, "J": 17}
	for col, wdth := range smwdth {
		f.SetColWidth("Sheet1", col, col, wdth)
	}
	for col, wdth := range hcwdth {
		f.SetColWidth("Sheet2", col, col, wdth)
		f.SetColWidth("Sheet3", col, col, wdth)
	}
}

func filling(corl string) int {
	styleI, _ := f.NewStyle(&excelize.Style{
		Border: []excelize.Border{
			{Type: "left", Color: "000000", Style: 1},
			{Type: "top", Color: "000000", Style: 1},
			{Type: "bottom", Color: "000000", Style: 1},
			{Type: "right", Color: "000000", Style: 1},
		},
		Alignment: &excelize.Alignment{
			Horizontal: corl,
			Vertical:   "center",
			WrapText:   true,
		},
		Font: &excelize.Font{
			Family: "宋体",
		},
	})
	return styleI
}

func styless() {
	styleIdc, _ := f.NewStyle(&excelize.Style{
		Alignment: &excelize.Alignment{
			Horizontal: "center",
		},
	})

	f.SetCellStyle("Sheet2", "A1", "A1", styleIdc)
	f.SetCellStyle("Sheet3", "A1", "A1", styleIdc)
}

func defaultKey(key, defval string, anymap map[string]string) string {
	_, exist := anymap[key]
	if exist {
		return anymap[key]
	} else {
		return defval
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

func fileExist(fl string) bool {
	if _, err := os.Stat(fl); err == nil {
		return true
	} else {
		return false
	}
}

func mvFile(file string) {
	dirname := fmt.Sprintf("done-%s", namedate)
	os.Mkdir(dirname, 0o755)
	newpath := fmt.Sprintf("%s/%s", dirname, file)
	if fileExist(file) {
		os.Rename(file, newpath)
	}
}

func mvFiles() {
	for _, pool := range pools {
		re := regexp.MustCompile("[0-9]+")
		nums := re.FindAllString(pool, -1)
		cfile := fmt.Sprintf("c%s.csv", nums[0])
		mvFile(cfile)
		hfile := fmt.Sprintf("h%s.csv", nums[0])
		mvFile(hfile)
		patn := "[ch]*.zip"
		files, _ := filepath.Glob(patn)
		for _, zipfile := range files {
			mvFile(zipfile)
		}
	}
}

func rmFile(file string) {
	if fileExist(file) {
		os.Remove(file)
	}
}

func rmFiles() {
	for _, file := range tmpfiles {
		rmFile(file)
	}
}

func renameZiles() {
	patn := "[ch]*.zip"
	files, _ := filepath.Glob(patn)
	for _, zipfile := range files {
		filename := strings.Replace(zipfile, ".zip", "", -1)
		zip.Unzip(zipfile, filename)
		csvpatn := filename + "/*/*.csv"
		csvname := filename + ".csv"
		files, _ := filepath.Glob(csvpatn)
		os.Rename(files[0], csvname)
		os.RemoveAll(filename)

		poolnum := toNum(getPool(csvname))
		prefix := filename[0:1]
		newcname := prefix + strconv.Itoa(poolnum) + ".csv"
		newzname := prefix + strconv.Itoa(poolnum) + ".zip"
		tmpfiles = append(tmpfiles, newcname)
		if poolnum != 0 {
			os.Rename(csvname, newcname)
			os.Rename(zipfile, newzname)
		}
	}
	remind()
}

func renameCiles() {
	patn := "[ch][ui][rs]*.csv"
	files, _ := filepath.Glob(patn)
	for _, csvfile := range files {
		poolnum := toNum(getPool(csvfile))
		prefix := csvfile[0:1]
		newcname := prefix + strconv.Itoa(poolnum) + ".csv"
		if poolnum != 0 {
			os.Rename(csvfile, newcname)
		}
	}
	remind()
}

func getPool(file string) string {
	cont := readFile(file)
	for _, line := range cont {
		for _, field := range line {
			re := regexp.MustCompile("-[0-9]{2}[aA]-")
			pl := re.FindString(field)
			if pl != "" {
				return pl
			}

		}
	}
	unget = append(unget, file)
	return "0"
}

func toNum(s string) int {
	re := regexp.MustCompile("[0-9]+")
	num := re.FindString(s)
	nu, _ := strconv.Atoi(num)

	return nu
}

func remind() {
	for _, file := range unget {
		fmt.Printf("程序不知道\033[42m%s\033[0m是哪个资源池的，但你一定知道，请勿退出程序，输入该资源池的编号后回车。\n", file)
		var poolnum string
		fmt.Scanln(&poolnum)
		newcname := file[0:1] + poolnum + ".csv"
		newzname := file[0:1] + poolnum + ".zip"
		os.Rename(file, newcname)
		os.Rename(strings.Replace(file, "csv", "zip", -1), newzname)
	}
}
