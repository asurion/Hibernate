<div id="main-content" class="wiki-content">
   <p style="text-align: left;">Save money by adding a tag to your <strong>ec2</strong> instances or <span style="color: rgb(0,0,0);"><strong>autoscaling groups</strong></span>. Sounds easy right? Cloud governance has come up with a simple solution to help your team put your instances to sleep(<em>stopped</em> <em>state</em>) when they are not being used, saving your team money.</p>
   <p style="text-align: left;">
   <div class="toc-macro client-side-toc-macro " data-headerelements="H1,H2,H3,H4,H5,H6,H7"></div>
   </p>
   <h1 style="text-align: left;" id="CostOptimization:SleepSchedule-EC2-Thingstoknowbeforeyougetstarted">Things to know before you get started</h1>
   <ul>
      <li style="text-align: left;"><strong><a href="http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html" class="external-link" rel="nofollow">http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html</a></strong></li>
      <li style="text-align: left;">When the scheduler executes on your auto scaling group, a snapshot of your current configuration will be saved and reused whenever your instance restart. (min,max,desired instance count)</li>
   </ul>
   <ol>
      <li style="text-align: left;">
         Resources you can tag:
         <ol>
            <li style="text-align: left;">Stand-alone ec2</li>
            <li style="text-align: left;">Elastic Beanstalk (If your environment already exists, just go tag the autoscaling group, and <strong>remember to add the scheduler tag to your next deployment</strong>)</li>
            <li style="text-align: left;">
               Auto Scaling Groups<br />
               <ol>
                  <li style="text-align: left;">
                     <p><span style="color: rgb(255,0,0);">You can easily turn your environment back on by altering the variables in your <strong>auto scaling group</strong> back to the original config. If the scheduler sleeps your environment, these values will appear to be a zero (0)… A new tag is also placed on your auto scaling group “scheduler:asg-previous:min,max,desired” which will hold the value of the previous configuration. (you do not need to edit the tag)</span></p>
                  </li>
               </ol>
            </li>
         </ol>
      </li>
   </ol>
   <p style="text-align: left;"> </p>
   <h1 id="CostOptimization:SleepSchedule-EC2-Quick-startguide"><strong>Quick-start guide</strong></h1>
   <ol>
      <li>
         Simply add the following tag key/value pair to your ec2 instance <strong>OR</strong> autoscaling group:
         <ol>
            <li><strong><u>TAG THE AUTO SCALING GROUP CONFIG IF YOUR INSTANCE(S) ARE ASSOCIATED WITH AN ASG (not the ec2 instance).</u></strong></li>
            <li>
               <div class="code panel pdl" style="border-width: 1px;">
                  <div class="codeHeader panelHeader pdl" style="border-bottom-width: 1px;"><b>tag</b></div>
                  <div class="codeContent panelContent pdl">
                     <script type="syntaxhighlighter" class="brush: java; gutter: false; theme: Confluence"><![CDATA[tag = [
                        {
                        &quot;Key&quot;:&quot;SCHEDULER:SLEEP&quot;,
                        &quot;Value&quot;:&quot;FOLLOWTHESUN&quot;
                        }
                        ]]]>
                     </script>
                  </div>
               </div>
            </li>
            <li>Key: <strong>SCHEDULER:SLEEP</strong></li>
            <li>Value: <strong>FOLLOWTHESUN</strong><strong><br /></strong></li>
         </ol>
      </li>
      <li>Description: 7:00pm Friday – 3:00pm Sunday, pacific time (pt) <u>44 hours of sleep!</u><strong><br /></strong></li>
      <li>This saves you over 25% a week per instance!!!</li>
      <li><em><strong>Remember to add this schedule to all of your scripts</strong></em></li>
   </ol>
   <p> </p>
   <hr />
   <h2 id="CostOptimization:SleepSchedule-EC2-Usingyourownsolution?">Using your own solution?</h2>
   <p>If your project team has already developed a method of putting your environments to sleep, that's okay!  We still require you to place this tag on your instances, but the value you'll use is:</p>
   <ul>
      <li>Key = <strong>&quot;SCHEDULER:SLEEP&quot;</strong></li>
      <li>Value = <strong>&quot;ALTERNATIVE&quot;</strong></li>
   </ul>
   <p> </p>
   <h2 id="CostOptimization:SleepSchedule-EC2-NotreadytoSleep?">Not ready to Sleep?</h2>
   <p>If your project team is not ready to put your EC2 resources to sleep on a regular schedule, we still require you to place this tag on your instances. The value you'll use to be skipped over during the sleep routine is:</p>
   <ul>
      <li>Key = <strong>&quot;SCHEDULER:SLEEP&quot;</strong></li>
      <li>Value = <strong>&quot;INACTIVE&quot;</strong></li>
   </ul>
   <p>Please note that by tagging your resources with an Inactive value, you'll be subject to regular check-ups about when you might be able to take advantage of the flexible nature of AWS to save money.  We appreciate that teams have a varied work schedules, but we believe that there are still plenty of opportunities at some point in a project's life cycle.</p>
   <p> </p>
   <h1 id="CostOptimization:SleepSchedule-EC2-AdvancedGuidetoCustomSchedules"><strong>Advanced Guide to Custom Schedules</strong></h1>
   <div class="code panel pdl" style="border-width: 1px;">
      <div class="codeHeader panelHeader pdl" style="border-bottom-width: 1px;"><b>tag</b></div>
      <div class="codeContent panelContent pdl">
         <script type="syntaxhighlighter" class="brush: java; gutter: false; theme: Confluence"><![CDATA[tag = [
            {
            &quot;Key&quot;:&quot;SCHEDULER:SLEEP&quot;,
            &quot;Value&quot;:&quot;&lt;HHHH;HHHH;tz;schedule&gt;&quot;
            }
            ]]]>
         </script>
      </div>
   </div>
   <p><u><strong>tag explained</strong></u></p>
   <div class="table-wrap">
      <table class="confluenceTable">
         <tbody>
            <tr>
               <th class="confluenceTh">HHHH;</th>
               <th class="confluenceTh">HHHH;</th>
               <th class="confluenceTh">tz;</th>
               <th class="confluenceTh">schedule</th>
               <th colspan="1" class="confluenceTh">&amp;</th>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">stop time</td>
               <td colspan="1" class="confluenceTd">start time</td>
               <td colspan="1" class="confluenceTd">timezone</td>
               <td colspan="1" class="confluenceTd">the pre-made schedules (weekends,weekdays, all) OR days of the week, comma separated (mon,wed,fri)</td>
               <td colspan="1" class="confluenceTd">adding the '&amp;' after a schedule will allow you to chain multiple schedules</td>
            </tr>
         </tbody>
      </table>
   </div>
   <p><u><strong>&quot;&amp;&quot; explained</strong></u></p>
   <ul>
      <li>the following is a valid schedule to stop instances on weekends BUT you have a job you need to run in saturday at 1pm</li>
   </ul>
   <ul>
      <li style="list-style-type: none;background-image: none;">
         <ul>
            <li>2000;0600;ct;weekends&amp;1500;1300;ct;sat</li>
         </ul>
      </li>
   </ul>
   <hr />
   <p><strong><u><br /></u></strong></p>
   <div class="table-wrap">
      <table class="confluenceTable">
         <tbody>
            <tr>
               <th colspan="1" class="confluenceTh"> </th>
               <th class="confluenceTh">followthesun</th>
               <th class="confluenceTh">weekends</th>
               <th class="confluenceTh">weekdays</th>
               <th class="confluenceTh">all</th>
               <th colspan="1" class="confluenceTh">(specific days of the week)</th>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">Key</td>
               <td class="confluenceTd">
                  <pre><strong>SCHEDULER:SLEEP</strong></pre>
               </td>
               <td class="confluenceTd">
                  <pre><strong>SCHEDULER:SLEEP</strong></pre>
               </td>
               <td class="confluenceTd">
                  <pre><strong>SCHEDULER:SLEEP</strong></pre>
               </td>
               <td class="confluenceTd">
                  <pre><strong>SCHEDULER:SLEEP</strong></pre>
               </td>
               <td colspan="1" class="confluenceTd">
                  <pre><strong>SCHEDULER:SLEEP</strong></pre>
               </td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">Value</td>
               <td class="confluenceTd">followthesun</td>
               <td class="confluenceTd">2000;0600;ct;weekends</td>
               <td class="confluenceTd">1800;0600;ct;weekdays</td>
               <td class="confluenceTd">2000;0600;ct;all</td>
               <td colspan="1" class="confluenceTd"><span>2000;0600;ct;mon,wed,fri</span></td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">Sleep<br />Description</td>
               <td colspan="1" class="confluenceTd">
                  <p>7:00pm Friday – 3:00pm Sunday,</p>
                  <p>pacific time (pt)</p>
               </td>
               <td colspan="1" class="confluenceTd">
                  <p>8:00pm Friday – 6:00am Monday,</p>
                  <p>central time (ct)</p>
               </td>
               <td colspan="1" class="confluenceTd">
                  <p>6:00pm – 6:00am mon,tue,wed,thu,fri,</p>
                  <p>(also sleeps the weekend until 6am monday)</p>
                  <p>central time (ct)</p>
               </td>
               <td colspan="1" class="confluenceTd">
                  <p>8:00pm – 6:00am everyday</p>
                  <p><span>central time (ct)</span></p>
               </td>
               <td colspan="1" class="confluenceTd">
                  <p>8:00pm – 6:00am Monday, Wednesday, Friday</p>
                  <p>central time (ct)</p>
               </td>
            </tr>
         </tbody>
      </table>
   </div>
   <p> </p>
   <p><strong>Available Timezones and days abbreviations</strong></p>
   <div class="table-wrap">
      <table class="confluenceTable">
         <tbody>
            <tr>
               <th class="confluenceTh">Region</th>
               <th colspan="1" class="confluenceTh">State/Country</th>
               <th class="confluenceTh">Time Zone Abbreviation</th>
               <th colspan="1" class="confluenceTh"> </th>
               <th colspan="1" class="confluenceTh"> </th>
               <th colspan="1" class="confluenceTh"> </th>
               <th colspan="1" class="confluenceTh"> </th>
               <th colspan="1" class="confluenceTh">Days <span>Abbreviation</span></th>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">us-east-1</td>
               <td colspan="1" class="confluenceTd">North Virginia</td>
               <td colspan="1" class="confluenceTd">et</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">mon</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">us-west-1,us-west-2</td>
               <td colspan="1" class="confluenceTd">North California, Oregon</td>
               <td colspan="1" class="confluenceTd">pt</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">tue</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">eu-west-1</td>
               <td colspan="1" class="confluenceTd">Ireland</td>
               <td colspan="1" class="confluenceTd">utc</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">wed</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">eu-central-1</td>
               <td colspan="1" class="confluenceTd">Frankfurt</td>
               <td colspan="1" class="confluenceTd">cet</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">thu</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">ap-southeast-1</td>
               <td colspan="1" class="confluenceTd">Singapore</td>
               <td colspan="1" class="confluenceTd">sgt</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">fri</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">ap-southeast-2</td>
               <td colspan="1" class="confluenceTd">Sydney</td>
               <td colspan="1" class="confluenceTd">aedt</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">sat</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd"><span>ap-northeast-1</span></td>
               <td colspan="1" class="confluenceTd">Tokyo</td>
               <td colspan="1" class="confluenceTd">jst</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">sun</td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">ap-northeast-2</td>
               <td colspan="1" class="confluenceTd">Seoul</td>
               <td colspan="1" class="confluenceTd">kt</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">ap-south-1</td>
               <td colspan="1" class="confluenceTd">Mumbai</td>
               <td colspan="1" class="confluenceTd">in</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">sa-east-1</td>
               <td colspan="1" class="confluenceTd">Sao Paulo</td>
               <td colspan="1" class="confluenceTd">brt</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
            </tr>
            <tr>
               <td colspan="1" class="confluenceTd">Central Time</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd">ct</td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
               <td colspan="1" class="confluenceTd"> </td>
            </tr>
         </tbody>
      </table>
   </div>
   <p> </p>
   <p> </p>
   <p><strong><br /></strong></p>
   <p><strong><u><br /></u></strong></p>
   <p> </p>
</div>