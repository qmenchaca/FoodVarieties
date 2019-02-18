from models import Base, User, Food, Variety, Characteristic
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///FoodVarieties.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


sweet = Characteristic(char='Sweet')
session.add(sweet)
session.commit()

tart = Characteristic(char='Tart')
session.add(tart)
session.commit()

tangy = Characteristic(char='Tangy')
session.add(tangy)
session.commit()

juicy = Characteristic(char='Juicy')
session.add(juicy)
session.commit()

mild = Characteristic(char='Mild')
session.add(mild)
session.commit()

bitter = Characteristic(char='Bitter')
session.add(mild)
session.commit()

storage = Characteristic(char='Good for Storage')
session.add(storage)
session.commit()

user = User(username='Not you',
            email='someotheremail@gmail.com')
session.add(user)
session.commit()


apple = Food(name='Apple',
             picture='http://www.mottsfresh.com/wp-content/uploads/2016/03/Apples864x573.jpg',
             protected=True)
session.add(apple)
session.commit()


var = Variety(name='Golden Delicious',
              description='Very sweet, green-yellow apple.',
              food=apple,
              characteristics=[sweet, mild, storage, juicy],
              picture='https://www.wegmans.com/content/dam/wegmans/products/569/92569.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Roxbury Russet',
              description="The first apple variety in America." \
                          " Great for making cider.",
              food=apple,
              characteristics=[sweet, tart, storage, tangy],
              picture='https://newenglandapples.files.wordpress.com/2011/12/roxbury_russet.jpg?w=100',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Jonagold',
              description="A recent cultivar, " \
                          "this apple is very popular in Europe.",
              food=apple,
              characteristics=[sweet, juicy, tart],
              picture='https://images-na.ssl-images-amazon.com/images/I/81JfUCij2US._SY355_.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Liberty',
              description='This reddish dessert apple is great for applesauce!',
              food=apple,
              characteristics=[tangy, juicy, tart],
              picture='http://files.recipetips.com/images/glossary/a/apple_liberty.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Calville Blanc',
              description='This apple may look odd, but it is delicious!',
              food=apple,
              characteristics=[tangy, juicy, tart],
              picture='https://static1.squarespace.com/static/5a458ce12aeba5a1e6ec379a/5a5d1335e2c483cd41c18100/5a5d1502085229750fd66975/1530818874520/Calville+Blanc+basin.JPG?format=100w',
              user=user)
session.add(var)
session.commit()


orange = Food(name='Orange',
              picture='https://images-na.ssl-images-amazon.com/images/I/51TcdS9z2fL._SY300_QL70_.jpg',
              protected=True)
session.add(orange)
session.commit()

var = Variety(name='Valencia',
              description="The only major orange variety harvested " \
                          "during the summer, it was developed in " \
                          "Southern California in the mid-19th century.",
              food=orange,
              characteristics=[sweet, juicy],
              picture='http://www.internationalcitrusandproduce.com/wp-content/uploads/2012/01/valencia-orange1.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Navel',
              description='This seedless orange is very popular for eating!',
              food=orange,
              characteristics=[bitter, storage, juicy],
              picture='http://fruitguys.com/sites/default/files/styles/large/public/wp-content/uploads/2012/05/navel_trans1.png?itok=WV76YKJ0',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Blood',
              description="The blood orange may long angry, " \
                          "but it is very rich in antioxidants.",
              food=orange,
              characteristics=[juicy, tangy],
              picture='http://rivista-cdn.hvmag.com//images/cache/cache_a/cache_4/cache_6/Fotolia_104580946_Subscription_Monthly_L-e5edc64a.jpeg?ver=1548031542&aspectratio=1.5009380863039',
              user=user)
session.add(var)
session.commit()


potato = Food(name='Potato',
              picture='https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2014/9/24/1411574454561/03085543-87de-47ab-a4eb-58e7e39d022e-620x372.jpeg?width=620&quality=85&auto=format&fit=max&s=5044068bd43d9363b44a5e4cecd5d8e6',
              protected=True)
session.add(potato)
session.commit()

var = Variety(name='Yukon Gold',
              description='This yellow potato is very verstaile for any recipe.',
              food=potato,
              characteristics=[storage, mild],
              picture='https://www.johnnyseeds.com/dw/image/v2/BBBW_PRD/on/demandware.static/-/Sites-jss-master/default/dw53c1c9e8/images/products/vegetables/0532_01_yukongold.jpg',
              user=user)
session.add(var)
session.commit()


var = Variety(name='Russian Banana',
              description="These funny-shaped potatoes are hard to grow, " \
                          "but worth the effort!",
              food=potato,
              characteristics=[storage, mild, sweet],
              picture='https://www.smartkitchen.com/assets/images/resources/large/1281720238Potatoes-Russian%20Banana%20Fingerling%20Potatoes.jpg',
              user=user)
session.add(var)
session.commit()


squash = Food(name='Squash',
              picture='https://whatscookingamerica.net/wp-content/uploads/2015/03/Butternut-Squash2.jpg',
              protected=True)
session.add(squash)
session.commit()


var = Variety(name='Butternut',
              description="This squash has a very beautiful orange color " \
                          "and is very sweet. " \
                          "Don't forget to save and roast the seeds!",
              food=squash,
              characteristics=[storage, sweet],
              picture='https://whatscookingamerica.net/wp-content/uploads/2015/03/Butternut-Squash2.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Acorn',
              description="This prettty squash is great for roasting " \
                          "and a perfect side dish for Thanksgiving!",
              food=squash,
              characteristics=[storage, mild, sweet],
              picture='https://assets.blog.foodnetwork.ca/imageserve/wp-content/uploads/sites/6/2017/09/acorn-squash/x.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Pumpkin',
              description="This squash is spooky when carved on Halloween, " \
                          "but mild and a natural filling for a pie in the kitchen.",
              food=squash,
              characteristics=[storage, mild, sweet],
              picture='https://assets.blog.foodnetwork.ca/imageserve/wp-content/uploads/sites/6/2017/09/sugar-pumpkin/x.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Delicata',
              description="As the name suggests, " \
                          "this squash is delicate and very creamy." \
                          " Absolutely delicious roasted.",
              food=squash,
              characteristics=[sweet, tangy],
              picture='https://holycowvegan.net/wp-content/uploads/2016/09/delicata-squash-1.jpg',
              user=user)
session.add(var)
session.commit()


apricot = Food(name='Apricot',
               picture='https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Apricot_and_cross_section.jpg/330px-Apricot_and_cross_section.jpg',
               protected=True)
session.add(squash)
session.commit()

var = Variety(name='Flavor Giant',
              description="The name ain't lying! A delicious sweet-tart " \
                          "flavor that harvests very early.",
              food=apricot,
              characteristics=[sweet, tart, juicy],
              picture='http://www.davewilson.com/sites/default/files/styles/product/public/products/full/flavor_giant.jpg?itok=4EvL-cIJ',
              user=user)
session.add(var)
session.commit()


var = Variety(name='Katy',
              description="These large fruits are great right off the tree!",
              food=apricot,
              characteristics=[sweet, tangy, juicy],
              picture='http://clausennursery.com/media/zoo/images/apricot_katy_dreamstime_20032574_926b997f76927ba1347ac48c0d295e05.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Brittany Gold',
              description="These apricots are VERY hardy, " \
                          "but difficult to grow.",
              food=apricot,
              characteristics=[sweet, storage, juicy],
              picture='https://smhttp-ssl-17653.nexcesscdn.net/media/catalog/product/cache/1/thumbnail/9df78eab33525d08d6e5fb8d27136e95/b/r/brittany-gold-rw07.jpg',
              user=user)
session.add(var)
session.commit()


banana = Food(name='Banana',
              picture='https://target.scene7.com/is/image/Target/GUEST_f5d0cfc3-9d02-4ee0-a6c6-ed5dc09971d1?wid=488&hei=488&fmt=webp',
              protected=True)
session.add(squash)
session.commit()

var = Variety(name='Cavendish',
              description="These are the most popular bananas in the Western" \
                          " world. Get noticeably sweeter as they ripen.",
              food=banana,
              characteristics=[mild, tangy],
              picture='https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Cavendish_Banana_DS.jpg/800px-Cavendish_Banana_DS.jpg',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Gros Michel',
              description="These bananas were once enjoyed worldwide, " \
                          "but are very suspectible to disease. " \
                          "Extremely sweet.",
              food=banana,
              characteristics=[storage, sweet],
              picture='https://cdn.shopify.com/s/files/1/1294/9917/products/image_1c150b4a-7d30-4aae-bf4c-55f26964cc51_394x.jpg?v=1509732389',
              user=user)
session.add(var)
session.commit()

var = Variety(name='Plantain',
              description="Very starchy, these bananas must be " \
                          "cooked before eaten. Delicious fried!",
              food=banana,
              characteristics=[storage, mild],
              picture='https://cdn3.volusion.com/kceqm.mleru/v/vspfiles/photos/166-2T.jpg?1521734349',
              user=user)
session.add(var)
session.commit()


with engine.connect() as con:
    s = con.execute('SELECT * FROM association')
    for row in s:
        print row
