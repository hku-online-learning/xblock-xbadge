"""This XBlock is designed for Customizable Badge Collections"""

import pkg_resources
import MySQLdb
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

from xblock.core import XBlock
from xblock.fields import Scope, Integer, String, List, Dict, Boolean
from xblock.fragment import Fragment
from django.template import Context, Template
from .settings import DB, MONGO, MYTITLE

import logging
log = logging.getLogger(__name__)

class XBadgeXBlock(XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.
    display_name = String(display_name="Display Name",
                          default="Badge",
                          scope=Scope.settings,
                          help="Name of the component in the edX platform")

    myBadges = List(display_name="myBadges",
                          default=[""],
                          scope=Scope.user_state,
                          help="URLs of Badges")

    myVideo = List(display_name="myVideo",
                   default=[""],
                   scope=Scope.user_state,
                   help="Missing Video")

    myQuiz = List(display_name="myQuiz",
                  default=[],
                  scope=Scope.user_state,
                  help="Incomplete Quiz")

    myFlag = List(display_name="myFlag",
                  default=[],
                  scope=Scope.user_state,
                  help="Flag of Completion")

    myTitle = List(display_name="myTitle",
                  default=MYTITLE,
                  scope=Scope.settings,
                  help="Title of Badges")

    myColor = List(display_name="myColor",
                   default=[],
                   scope=Scope.settings,
                   help="URLs of Colorful Images")

    myGrey = List(display_name="myGrey",
                   default=[],
                   scope=Scope.settings,
                   help="URLs of Grey Images")

    nBadges = Integer(display_name="nBadges",
                      default = 7,
                      scope=Scope.settings,
                      help="Total Number of Badges")

    myCourseNum = String(display_name="myCourseNum",
                          default="TypeTheCourseNumHere",
                          scope=Scope.settings,
                          help="Which course is selected")

    myCourseRun = String(display_name="myCourseRun",
                         default="Please type the correct CourseNum",
                         scope=Scope.settings,
                         help="Which run is selected")

    videoArr = List(display_name="videoArr",
                  default=[],
                  scope=Scope.settings,
                  help="Video Array")

    quizArr = List(display_name="quizArr",
                    default=[],
                    scope=Scope.settings,
                    help="Quiz Array")

    videoDic = Dict(display_name="videoDic",
                   default={},
                   scope=Scope.settings,
                   help="Video Dictionary")

    quizDic = Dict(display_name="quizDic",
                    default={},
                    scope=Scope.settings,
                    help="Quiz Dictionary")

    videoMap = List(display_name="videoMap",
                    default=[],
                    scope=Scope.settings,
                    help="Video Mapping")

    quizMap = List(display_name="quizMap",
                    default=[],
                    scope=Scope.settings,
                    help="Quiz Mapping")

    quizPass = Integer(display_name="quizPass",
                      default = 50,
                      scope=Scope.settings,
                      help="Score for Quiz Pass")

    myReset = Boolean(display_name="quizPass",
                      default = True,
                      scope=Scope.settings,
                      help="Reset Status")

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the XBadgeXBlock, shown to students
        when viewing courses.
        """
        # Setup for local images
        local_resource_url0 = []
        local_resource_url1 = []
        if self.myReset:
            for i in range(self.nBadges):
                local_resource_url0.append(self.runtime.local_resource_url(self, 'public/images/Badge_A_Gray.png'))
                local_resource_url1.append(self.runtime.local_resource_url(self, 'public/images/Badge_A_Color.png'))

        # Get current student id
        STUDENT_ID = self.scope_ids.user_id
        if not isinstance(STUDENT_ID, (int, long)):
            STUDENT_ID = 31

        if 'passwd' in DB:
            db = MySQLdb.connect(host=DB['host'], user=DB['user'], passwd=DB['passwd'], db=DB['db'])
        else:
            db = MySQLdb.connect(host=DB['host'], user=DB['user'], db=DB['db'])
        cur = db.cursor()

        # Find COURSE_ID
        part1 = "SELECT id FROM course_overviews_courseoverview WHERE id LIKE '%"
        part2 = "%'"
        query = part1 + self.myCourseNum + "+" + self.myCourseRun + part2
        cur.execute(query)

        COURSE_ID = ""
        for row in cur.fetchall():
            COURSE_ID = row[0]

        # Get course structure
        CHA_video = []
        try:
            for j in range(self.nBadges):
                temp_video = []
                for i in range(len(self.videoArr)):
                    if self.videoMap[i][j] == 1:
                        temp = self.videoDic.keys()[self.videoDic.values().index(self.videoArr[i])]
                        temp_video.append(temp)
                CHA_video.append(temp_video)
        except:
            CHA_video = []

        CHA_quiz = []
        try:
            for j in range(self.nBadges):
                temp_quiz = []
                for i in range(len(self.quizArr)):
                    if self.quizMap[i][j] == 1:
                        temp = self.quizDic.keys()[self.quizDic.values().index(self.quizArr[i])]
                        temp_quiz.append(temp)
                CHA_quiz.append(temp_quiz)
        except:
            CHA_quiz = []

        # Check Video Watched
        part1 = "SELECT module_id FROM courseware_studentmodule WHERE course_id = '"
        part2 = "' AND student_id = "
        part3 = " AND module_type = 'video';"
        query = part1 + COURSE_ID + part2 + str(STUDENT_ID) + part3
        cur.execute(query)
        flag_video = []
        student_video = []

        for row in cur.fetchall():
            student_video.append(row[0])

        temp = []
        try:
            videoLen = max(32,len(CHA_video[0][0]))
            for v in student_video:
                temp.append(v[-videoLen:])
        except:
            temp = []

        miss_video = []
        try:
            for value in CHA_video:
                if len(list(set(temp) & set(value))) >= len(value):
                    i = 1
                else:
                    i = 0
                flag_video.append(i)
                for require in value:
                    if require not in temp:
                        miss_video.append(require)
        except:
            flag_video = [0] * self.nBadges

        display_list = []
        for chapter in CHA_video:
            myString = ""
            for video_id in chapter:
                if video_id in miss_video:
                    myString += self.videoDic[video_id] + ". "
            display_list.append(myString.decode('utf-8'))

        self.myVideo = display_list

        # Check Quiz Passed
        query = "SELECT grade,max_grade,module_id FROM courseware_studentmodule WHERE max_grade >0 AND course_id = '" + COURSE_ID + "';"
        cur.execute(query)
        for row in cur.fetchall():
            try:
                sample_quiz = row[2]
            except:
                sample_quiz = ""

        new_CHA_quiz = []
        try:
            prefix = sample_quiz[0:-videoLen]
            for chapter in CHA_quiz:
                new_quiz = []
                for quiz_id in chapter:
                    if len(quiz_id) == videoLen:
                        temp = prefix + quiz_id
                        new_quiz.append(temp.encode('UTF-8'))
                new_CHA_quiz.append(new_quiz)
            part1 = "SELECT grade,max_grade,module_id FROM courseware_studentmodule WHERE max_grade >0 AND course_id = '"
            part1a = "'"
            part2 = " AND student_id = "
            part3 = " AND module_id "
            part4 = ";"
            flag_quiz = []
            for quiz in new_CHA_quiz:
                if len(quiz) > 1:
                    part3a = "in "
                    part3b = " GROUP BY module_id"
                    partx = tuple(quiz)
                elif len(quiz) == 1:
                    part3a = "= '"
                    part3b = "' GROUP BY module_id"
                    partx = quiz[0]
                else:
                    flag_quiz.append(1)
                    continue
                query = part1 + COURSE_ID + part1a + part3 + part3a + str(partx) + part3b + part4
                cur.execute(query)
                y = 0
                for row in cur.fetchall():
                    try:
                        y += int(row[1])
                    except:
                        y = y
                query = part1 + COURSE_ID + part1a + part2 + str(STUDENT_ID) + part3 + part3a + str(partx) + part3b + part4
                cur.execute(query)
                x = 0
                for row in cur.fetchall():
                    try:
                        x += int(row[0])
                    except:
                        x = x
                if y == 0:
                    flag_quiz.append(1)
                elif float(x) / float(y) >= self.quizPass/100.0:
                    flag_quiz.append(1)
                else:
                    flag_quiz.append(0)
        except:
            flag_quiz = [1] * self.nBadges

        self.myQuiz = flag_quiz

        # Check Badge Earned
        my_flag = []
        for i in range(self.nBadges):
            try:
                my_flag.append(flag_video[i]*flag_quiz[i])
            except:
                my_flag.append(0)

        self.myFlag = my_flag

        db.close()

        # Link to Images
        local_resource_url = []
        try:
            for i in range(self.nBadges):
                if my_flag[i] == 1:
                    if self.myReset:
                        local_resource_url.append(local_resource_url1[i])
                    else:
                        local_resource_url.append(self.myColor[i])
                else:
                    if self.myReset:
                        local_resource_url.append(local_resource_url0[i])
                    else:
                        local_resource_url.append(self.myGrey[i])
        except:
            local_resource_url = []

        self.myBadges = local_resource_url

        # Render student view
        html_charts = self.resource_string("public/html/xbadge.html")
        template = Template(html_charts)
        html = template.render(Context({
        }))
        frag = Fragment(html)
        frag.add_css(self.resource_string("public/css/xbadge.css"))
        frag.add_javascript(self.resource_string("public/js/src/xbadge.js"))
        frag.initialize_js('XBadgeXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.

    def studio_view(self, context=None):
        html_edit_chart = self.resource_string("public/html/xbadge_edit.html")
        template = Template(html_edit_chart)

        html = template.render(Context({
            'nBadges': self.nBadges,
            'myTitle': self.myTitle,
            'myColor':self.myColor,
            'myGrey':self.myGrey,
            'myCourseNum': self.myCourseNum,
            'myCourseRun': self.myCourseRun,
            'quizPass':self.quizPass,
        }))

        frag = Fragment(html.format(self=self))
        # adding references to external css and js files
        frag.add_css(self.resource_string("public/css/xbadge_edit.css"))
        frag.add_javascript(self.resource_string("public/js/src/xbadge_edit.js"))
        frag.initialize_js('XBadgeXBlockEdit')
        return frag

    @XBlock.json_handler
    def save_Settings(self, data, suffix=''):
        """
        Handler which saves the json data into XBlock fields.
        """
        if not (data['myTitle'] is None):
            self.myTitle = data['myTitle']

        if not (data['myColor'] is None):
            self.myColor = data['myColor']

        if not (data['myGrey'] is None):
            self.myGrey = data['myGrey']

        if not (data['nBadges'] is None):
            self.nBadges = data['nBadges']

        if not (data['myCourseNum'] is None):
            self.myCourseNum = data['myCourseNum']

        if not (data['myCourseRun'] is None):
            self.myCourseRun = data['myCourseRun']

        if not (data['videoArr'] is None):
            self.videoArr = data['videoArr']

        if not (data['quizArr'] is None):
            self.quizArr = data['quizArr']

        if not (data['videoMap'] is None):
            self.videoMap = data['videoMap']

        if not(data['quizMap'] is None):
            self.quizMap = data['quizMap']

        if not (data['quizPass'] is None):
            self.quizPass = data['quizPass']

        self.myReset = False

        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def send_Data(self, data, suffix=''):
        """
        Handler which sends data back to the javascript of student view
        """
        return {
                   'result': 'success',
                   'myBadges': self.myBadges,
                    'myVideo':self.myVideo,
                    'myQuiz':self.myQuiz,
                    'myFlag':self.myFlag,
                    'myTitle':self.myTitle,
                    'myCourseNum':self.myCourseNum,
                    'myCourseRun':self.myCourseRun,
                    'nBadges':self.nBadges,
                    'quizPass':self.quizPass,
        }

    @XBlock.json_handler
    def send_Edit(self, data, suffix=''):
        """
        Handler which sends data back to the javascript of studio view
        """

        return {
            'result': 'success',
            'myTitle': self.myTitle,
            'myColor':self.myColor,
            'myGrey':self.myGrey,
            'nBadges':self.nBadges,
            'myCourseNum': self.myCourseNum,
            'myCourseRun': self.myCourseRun,
            'videoArr':self.videoArr,
            'quizArr':self.quizArr,
            'videoMap': self.videoMap,
            'quizMap':self.quizMap,
        }

    @XBlock.json_handler
    def check_Course(self, data, suffix=''):
        """
        Handler which returns course runs.
        """
        result = 'success'
        if not (data['myCourseNum'] is None):
            myCourseNum = data['myCourseNum']
        else:
            result = 'failure'

        list_run = []
        try:
            client = MongoClient('localhost', 27017)
            active = client[MONGO['db']]['modulestore.active_versions']
            course_runs = active.find({'course':myCourseNum},{'run':1})
            for run in course_runs:
                list_run.append(run['run'])
            if len(list_run)==0:
                result = 'failure'
            client.close()
        except:
            result = 'failure'

        return {
            'result': result,
            'myCourseNum':myCourseNum,
            'list_run':list_run
        }

    @XBlock.json_handler
    def show_Map(self, data, suffix=''):
        """
        Handler which gets the data from studio and show badge mapping
        """
        result = 'success'
        if (data['nBadges'] is None):
            result = 'failure'
        if (data['myCourseNum'] is None):
            result = 'failure'
        if (data['myCourseRun'] is None):
            result = 'failure'

        courseStructure = []
        try:
            client = MongoClient(MONGO['host'], MONGO['port'])
            active = client[MONGO['db']]['modulestore.active_versions']
            course_info = active.find_one({'course': data['myCourseNum'], 'run':data['myCourseRun']})
            published = course_info['versions']['published-branch']

            structure = client[MONGO['db']]['modulestore.structures']
            course_file = structure.find_one({'_id': published})

            for block in course_file['blocks']:
                if block['block_type'] == 'course':
                    myCourse = block

            tempChapter = myCourse['fields']['children']

            listChapter = []
            for temp in tempChapter:
                if temp[0] == 'chapter':
                    listChapter.append(temp[1])

            for chapter in listChapter:
                for block in course_file['blocks']:
                    if block['block_id'] == chapter:
                        tempSequential = block['fields']['children']
                listSequential = []
                for temp in tempSequential:
                    if temp[0] == 'sequential':
                        listSequential.append(temp[1])
                resultSequential = []
                for sequential in listSequential:
                    tempVertical = []
                    for block in course_file['blocks']:
                        if block['block_id'] == sequential:
                            tempVertical = block['fields']['children']
                    listVertical = []
                    for temp in tempVertical:
                        if temp[0] == 'vertical':
                            listVertical.append(temp[1])
                    resultVertical = []
                    for vertical in listVertical:
                        tempModule = []
                        for block in course_file['blocks']:
                            if block['block_id'] == vertical:
                                tempModule = block['fields']['children']
                        listVideo = []
                        listQuiz = []
                        for temp in tempModule:
                            if temp[0] == 'video':
                                listVideo.append(temp[1].encode('utf-8'))
                            elif temp[0] == 'problem':
                                listQuiz.append(temp[1].encode('utf-8'))
                        resultVertical.append([listVideo, listQuiz])
                    resultSequential.append(resultVertical)
                courseStructure.append(resultSequential)

            client.close()

            videoArr = []
            videoDic = {}
            quizArr = []
            quizDic = {}
            for idxC, chapter in enumerate(courseStructure):
                for idxS, sequential in enumerate(chapter):
                    for idxT, vertical in enumerate(sequential):
                        for idxV, video in enumerate(vertical[0]):
                            labelV = '' + str(idxC + 1) + '-' + str(idxS + 1) + '-' + str(idxT + 1) + '-' + str(
                                idxV + 1)
                            videoArr.append(labelV)
                            videoDic.update({video: labelV})
                        for idxQ, quiz in enumerate(vertical[1]):
                            labelQ = '' + str(idxC + 1) + '-' + str(idxS + 1) + '-' + str(idxT + 1) + '-' + str(
                                idxQ + 1)
                            quizArr.append(labelQ)
                            quizDic.update({quiz: labelQ})
            self.videoArr = videoArr
            self.videoDic= videoDic
            self.quizArr = quizArr
            self.quizDic = quizDic
        except:
            return {'result' : 'failure'}

        return{
            'result':result,
            'videoArr':self.videoArr,
            'quizArr':self.quizArr,
            'videoMap':self.videoMap,
            'quizMap':self.quizMap,
        }

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
                ("XBadgeXBlock",
                 """<xbadge/>
                 """),
            ]
