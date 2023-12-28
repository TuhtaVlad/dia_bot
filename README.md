# jb_int_dia_bot
## PROBLEM
  Diabetes is a serious, chronic disease that occurs either when the pancreas does not produce enough insulin (a hormone that regulates blood sugar, or glucose), or when the body cannot effectively use the insulin it produces. Diabetes is an important public health problem, one of four priority noncommunicable diseases (NCDs) targeted for action by world leaders. Both the number of cases and the prevalence of diabetes have been steadily increasing over the past few decades.
  
## GLOBAL BURDEN 
  Globally, an estimated 422 million adults were living with diabetes in 2014, compared to 108 million in 1980. The global prevalence (age-standardized) of diabetes has nearly doubled since 1980, rising from 4.7% to 8.5% in the adult population. This reflects an increase in associated risk factors such as being overweight or obese. Over the past decade, diabetes prevalence has risen faster in low- and middle-income countries than in high-income countries. 
  Diabetes caused 1.5 million deaths in 2012. Higher-than-optimal blood glucose caused an additional 2.2 million deaths, by increasing the risks of cardiovascular and other diseases. Forty-three percent of these 3.7 million deaths occur before the age of 70 years. The percentage of deaths attributable to high blood glucose or diabetes that occurs prior to age 70 is higher in low- and middle-income countries than in high-income countries.
  Because sophisticated laboratory tests are usually required to distinguish between type 1 diabetes (which requires insulin injections for survival) and type 2 diabetes (where the body cannot properly use the insulin it produces), separate global estimates of diabetes prevalence for type 1 and type 2 do not exist. The majority of people with diabetes are affected by type 2 diabetes. This used to occur nearly entirely among adults, but now occurs in children too.

## COMPLICATIONS 
  Diabetes of all types can lead to complications in many parts of the body and can increase the overall risk of dying prematurely. Possible complications include heart attack, stroke, kidney failure, leg amputation, vision loss and nerve damage. In pregnancy, poorly controlled diabetes increases the risk of fetal death and other complications.
  
## ECONOMIC IMPACT 
  Diabetes and its complications bring about substantial economic loss to people with diabetes and their families, and to health systems and national economies through direct medical costs and loss of work and wages. While the major cost drivers are hospital and outpatient care, a contributing factor is the rise in cost for analogue insulins 1 which are increasingly prescribed despite little evidence that they provide significant advantages over cheaper human insulins.

Taken from the WHO report of 2016, dedicated to World Health Day: https://apps.who.int/iris/rest/bitstreams/909883/retrieve (Global report on diabetes (who.int))

At the same time, overweight and obesity are the strongest risk factors for developing type 2 diabetes.
Worldwide obesity has nearly tripled since 1975.
In 2016, more than 1.9 billion adults, 18 years and older, were overweight. Of these over 650 million were obese.
39% of adults aged 18 years and over were overweight in 2016, and 13% were obese.
Most of the world's population live in countries where overweight and obesity kills more people than underweight.
39 million children under the age of 5 were overweight or obese in 2020.
Over 340 million children and adolescents aged 5-19 were overweight or obese in 2016.
Obesity is preventable.

Taken from a post from the official WHO website dated June 9, 2021: Obesity and overweight (who.int)

## The purpose of the BOT
Based on all of the above, we believe that the problem of diabetes mellitus is very relevant in the modern world. It is very difficult to keep records of changes in blood sugar, since the majority of the population does not have access to gadgets that communicate with the phone and transmit all the information to it. I have to write down all the measurements on a piece of paper (I myself have repeatedly encountered similar situations). 
This bot was conceived as an assistant for keeping records of all criteria that affect blood sugar content.

## some AI capabilities
  Unfortunately, I could not independently implement the idea using "some AI capabilities". I could not implement it on my own (at least I do not have data for training a bot).
  The essence of the idea is to predict the development of a trend in the blood sugar content of a diabetic to avoid hypoglycemia and hyperglycemia. Based on data: gender, age, height, weight, body mass index, type of diabetes (or lack thereof), as well as data on sugar dynamics depending on food intake and injected insulin, we train our AI. After that, our AI builds a trend and indicates the predicted measurements and the approximate time of an excessive decrease (increase) in sugar levels based on the patient's personal data. 
  
The data that AI works with: 
  1. Sex
  2. Age
  3. Height
  4. Weight
  5. Body mass index(BMI)
  6. Type of diabetes
Type 1 diabetes (previously known as insulin-dependent, juvenile or childhood-onset diabetes) is characterized by deficient insulin production in the body. People with type 1 diabetes require daily administration of insulin to regulate the amount of glucose in their blood. If they do not have access to insulin, they cannot survive. The cause of type 1 diabetes is not known and it is currently not preventable. Symptoms include excessive urination and thirst, constant hunger, weight loss, vision changes and fatigue.
Type 2 diabetes (formerly called non-insulin-dependent or adult-onset diabetes) results from the body’s ineffective use of insulin. Type 2 diabetes accounts for the vast majority of people with diabetes around the world. Symptoms may be similar to those of type 1 diabetes, but are often less marked or absent. As a result, the disease may go undiagnosed for several years, until complications have already arisen. For many years type 2 diabetes was seen only in adults but it has begun to occur in children.

Taken from the WHO report of 2016, dedicated to World Health Day: https://apps.who.int/iris/rest/bitstreams/909883/retrieve (Global report on diabetes (who.int)) 

  7. Table: Blood glucose dynamics before eating - Meal(Carbohydrate counting) - Blood glucose dynamics after eating - Injected insulin - Blood glucose dynamic after injected insulin
This table will show the entire blood glucose dynamics relative to meals and injected insulin.

  Carbohydrate counting is a conventional unit that is used to approximate the amount of carbohydrates in foods: one CC is equal to 12 grams of carbohydrates or 25 grams of bread. One CC increases blood glucose levels by an average of 2 mmol/l. According to the system of Bread Units, those products that we refer to the group of those that increase blood sugar (cereals, fruits, liquid dairy products, potatoes, corn, sweets) are counted. For the convenience of compiling the menu, there are special tables of Bread Units, which provide data on the number of different carbohydrate-containing products containing 1 CC.
  To understand how much insulin needs to be injected, you need to take the difference between the actual and target glycemia and divide it by the sensitivity factor. Then we get the amount of insulin that needs to be injected. When blood sugar is higher than the target, a positive result is always obtained, which means that you need to add insulin to decrease. If there is active insulin, then it must be subtracted from the resulting number.
  If the blood sugar before eating is below the target, a negative number will be obtained, in this case we should reduce the dose for food by the resulting number.
